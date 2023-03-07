#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Kev.in - a coding learning platform
# Copyright (C) 2022 to 2023  Max Linke and others
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import ctypes
import importlib.util
import os
import sys
import threading
import time
from inspect import getmembers, isfunction
from typing import Type

from RestrictedPython import CompileResult, compile_restricted_exec, limited_builtins, safe_builtins, utility_builtins
from wrapt_timeout_decorator import *

__all__ = ["ExecutePython"]
_FORBIDDEN_MODULES = frozenset(
    (
        "os",
        "sys",
    )
)  # forbidden modules


def _safe_import(*name: tuple):
    """intercept non-allowed user-defined imports e.g. 'import os'"""
    user_import = name[0]
    if user_import in _FORBIDDEN_MODULES:
        raise ImportError(f"Don't even think about using {user_import!r}")
    return __import__(user_import)


class ExecutePython:
    def __init__(self):
        self.__sandbox_logs = dict()
        self.__sandbox_logs["COMPILERLOG"] = dict()
        self.__sandbox_logs["EXECUTELOG"] = dict()
        self.__sandbox_logs["RESULTLOG"] = dict()
        self.__sandbox_logs["EXECUTELOG"]["ERROR"] = tuple()
        self.__compile_result = CompileResult(None, None, None, None)

    @staticmethod
    def __check_timeout_on_windows(timeout_value, thread_for_windows: threading.Thread, exception: Type[BaseException]):
        """Executed by main thread, which observes the execution time of worker thread."""
        sleep_time = 0
        while thread_for_windows.is_alive():
            sleep_time = sleep_time + 1
            time.sleep(1)
            if sleep_time == timeout_value:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(thread_for_windows.ident), ctypes.py_object(exception)
                )

    @staticmethod
    def __timeout_user_code_exec(timeout_decorator_func, os_name: str):
        """If Windows OS, we ignore the timeout_decorator function, which is only supported on Linux."""

        def timeout_decorator(exec_byte_code):
            if os.name == "nt":
                return exec_byte_code
            # timeout decorator is executed
            return timeout_decorator_func(exec_byte_code)

        return timeout_decorator

    def exec_untrusted_code(self, user_code: str, user_func: str, *args_list) -> dict:
        """
        Description: Executed user code in restricted environment.

        :arg:
            user_code: String containing user code.
            user_func: Function inside user_code to execute and return value.
            *args_list: Nested list of arguments passed to the user function.

        :return:
        {'COMPILERLOG': {'ERROR': (), 'WARNINGS': []}, 'EXECUTELOG': {'ERROR': ()},
                                'RESULTLOG': {'0': [['arg0'], ['solution0']], ...}}

        Example
        Args:
            user_code: "def multiply(x,y):\r\n  return x*y"
            user_func: "multiply"
            *args_list: [[0,0], [1,0], [2,2], [3,3]]

        Return:
            {
            'COMPILERLOG': {
                            'ERROR': (), 'WARNINGS': []
                            },
            'EXECUTELOG': {
                            'ERROR': ()
                            },
            'RESULTLOG': {
                        '0': [[0,0], [0]],
                        '1': [[1,0], [0]],
                        '2': [[2,2], [4]],
                        '3': [[3,3], [9]]
                        }
            }
        """

        # Create usercode.py where user code is stored.
        f = open("usercode.py", "w")
        f.write(user_code)
        f.close()

        # Adds another lines to user code that executes user function.
        for args in args_list:
            user_code += "\nresult.append({0}({1}))".format(user_func, ",".join(map(str, args)))

        # Compile code.
        self.__compile_result = compile_restricted_exec(source=user_code)
        self.__sandbox_logs["COMPILERLOG"]["ERROR"] = self.__compile_result[1]
        self.__sandbox_logs["COMPILERLOG"]["WARNINGS"] = self.__compile_result[2]

        # Compilation failed.
        if self.__compile_result.code is None:
            if os.path.exists("usercode.py"):
                os.remove("usercode.py")
            return self.__sandbox_logs

        # Import module "usercode.py" as it is now safe to import.
        spec = importlib.util.spec_from_file_location("usercode", "./usercode.py")
        user_mod = importlib.util.module_from_spec(spec)
        sys.modules["usercode"] = user_mod
        spec.loader.exec_module(user_mod)
        user_defined_func = dict(getmembers(user_mod, isfunction))

        if os.path.exists("usercode.py"):
            os.remove("usercode.py")

        # If you want the user to be able to use some of your functions inside his code.
        # You should add this function to this dictionary.
        restricted_globals = {
            "__builtins__": {
                # **safe_builtins,
                **utility_builtins,
                **user_defined_func,  # allow all user-defined functions
                "__import__": _safe_import,
            },
            "_getiter_": iter,
            "_getattr_": getattr,
        }

        # This are the variables we allow the user code to see. @result will contain return value.
        restricted_locals = {
            "result": list(),
        }

        if os.name == "nt":  # multithreading
            """Untrusted user code is executed not in main thread. The main thread is responsible to check the
            execution time of the created worker thread "thread_for_windows". This worker thread executes the
            untrusted user code and if the execution time takes to long the main thread will interrupt the worker
            thread by throwing a TimeoutError. The worker thread handles this TimeoutError through the exception
            "TimeoutError" in __exec_byte_code and finally terminates. Due to the lack of signals on Windows, we
             cannot use the warp_timeout_decorator module, which uses signals. We are forced to use multithreading."""
            thread_for_windows = threading.Thread(
                target=self.__exec_byte_code,
                args=(
                    restricted_globals,
                    restricted_locals,
                    *args_list,
                ),
            )
            thread_for_windows.start()
            self.__check_timeout_on_windows(5, thread_for_windows, TimeoutError)
            return self.__sandbox_logs
        else:
            """Since this is not Windows, we can use the default function call and use the timeout decorator as Linux
            support signals."""
            return self.__exec_byte_code(restricted_globals, restricted_locals, *args_list)

    @__timeout_user_code_exec(timeout(4, timeout_exception=TimeoutError), os.name)
    def __exec_byte_code(self, restricted_globals: dict, restricted_locals: dict, *args_list: list) -> dict:
        if self.__compile_result.code is None:  # in case it's 'None', but should never become true.
            return self.__sandbox_logs

        try:
            # Run code
            exec(self.__compile_result.code, restricted_globals, restricted_locals)

        except TimeoutError:
            if os.path.exists("usercode.py"):
                os.remove("usercode.py")

            # code execution took too long
            self.__sandbox_logs["EXECUTELOG"]["ERROR"] = (
                "TimeoutError: Code execution has been interrupted. Maximum execution time has been reached!",
            )
            return self.__sandbox_logs

        except:
            if os.path.exists("usercode.py"):
                os.remove("usercode.py")

            # The code did something that is not allowed. Runtime error in code.
            import traceback

            type_, value_, traceback_ = sys.exc_info()

            self.__sandbox_logs["EXECUTELOG"]["ERROR"] = (value_,)
            return self.__sandbox_logs

        else:
            for idx, arg in enumerate(args_list):
                self.__sandbox_logs["RESULTLOG"][f"{idx}"] = [
                    arg,
                    [restricted_locals["result"][idx]],
                ]

            return self.__sandbox_logs
