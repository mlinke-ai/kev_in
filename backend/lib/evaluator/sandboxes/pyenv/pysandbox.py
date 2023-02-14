import importlib.util
import os
import sys
import re

from RestrictedPython import compile_restricted_exec
from RestrictedPython import limited_builtins, utility_builtins, safe_builtins
from RestrictedPython import CompileResult, compile_restricted_exec, utility_builtins

from inspect import getmembers, isfunction
import timeout_decorator


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

    def exec_untrusted_code(self, user_code: str, user_func: str, *args_list) -> dict:
        """
        Description: Executed user code in restricted environment.

        Args:
            user_code: String containing user code.
            user_func: Function inside user_code to execute and return value.
            *args_list: Nested list of arguments passed to the user function.

        Return:
        {'COMPILERLOG': {'ERROR': (), 'WARNINGS': []}, 'EXECUTELOG': {'ERROR': ()},
                                'RESULTLOG': {'0': [['arg0'], ['solution0']], ...}}

        Example
        Args:
            user_code: "def multiply(x,y):\r\n  return x*y"
            user_func: "def multiply(x,y):\r\n  pass"
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

        # Extract function name from function head by using regular expression.
        matchObject = re.search("(?<=def.).[a-z|A-Z|_]+[^\(]", user_func)
        if matchObject:
            user_func = matchObject.group(0)
        else:
            raise ValueError("User function does not have the form 'def fun(..):'")

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
        return self.__exec_byte_code(restricted_globals, restricted_locals, *args_list)

    @timeout_decorator.timeout(3.0, timeout_exception=TimeoutError)  # seconds
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
