import importlib.util
import sys

from RestrictedPython import compile_restricted_exec
from RestrictedPython import limited_builtins, utility_builtins, safe_builtins
from inspect import getmembers, isfunction
from RestrictedPython import CompileResult

import timeout_decorator

__all__ = ["ExecutePython"]
_SAFE_MODULES = frozenset(("math",))  # allowed modules to use
_FORBIDDEN_MODULES = frozenset(("os", "sys",))  # forbidden modules


def _safe_import(*name: tuple):
    """intercept non-allowed user-defined imports e.g. 'import os'"""
    user_import = name[0]
    if user_import in _FORBIDDEN_MODULES:
        raise ImportError(f"Don't even think about using {user_import!r}")
    return __import__(user_import)


class ExecutePython:

    def __init__(self):
        self.__sandbox_logs = None
        self.__sandbox_logs = dict()
        self.__sandbox_logs["COMPILERLOG"] = dict()
        self.__sandbox_logs["EXECUTELOG"] = dict()
        self.__sandbox_logs["RESULTLOG"] = dict()
        self.__compile_result = CompileResult(None, None, None, None)

    def exec_untrusted_code(self, filename: str, user_func: str, *args_list) -> dict:
        """ Executed user code in restricted env.
        Args:
            filename(str) - String containing filename.
            user_func(str) - Function inside user_code to execute and return value.
            *args_list - Nested list of arguments passed to the user function.
        """
        # Generate user code as str.
        with open(filename, "r") as f:
            user_code = f.read()

        # Adds another lines to user code that executes user function.
        for args in args_list:
            user_code += "\nresult.append({0}({1}))".format(user_func, ','.join(map(str, args)))

        # Compile code.
        self.__compile_result = compile_restricted_exec(source=user_code, filename=filename)
        self.__sandbox_logs["COMPILERLOG"]["ERROR"] = self.__compile_result[1]
        self.__sandbox_logs["COMPILERLOG"]["WARNINGS"] = self.__compile_result[2]

        # Compilation failed.
        if self.__compile_result.code is None:
            return self.__sandbox_logs

        # Import module "usercode.py" as it is now safe to import.
        spec = importlib.util.spec_from_file_location("usercode", "./backend/lib/userCodeExecution/usercode.py")
        user_mod = importlib.util.module_from_spec(spec)
        sys.modules["usercode"] = user_mod
        spec.loader.exec_module(user_mod)
        user_defined_func = dict(getmembers(user_mod, isfunction))

        # If you want the user to be able to use some of your functions inside his code.
        # You should add this function to this dictionary.
        restricted_globals = {
            "__builtins__": {
                # **safe_builtins,
                **utility_builtins,
                **user_defined_func,  # allow all user-defined function? Or only the one we specify e.g. "fib"
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

        # except:
        #     # catch *all* exceptions
        #     import traceback
        #     type_, value_, traceback_ = sys.exc_info()
        #
        #     self.__sandbox_logs["COMPILERLOG"]["ERROR"] = value_
        #     return self.__sandbox_logs

    @timeout_decorator.timeout(5.0, timeout_exception=TimeoutError)  # seconds
    def __exec_byte_code(self, restricted_globals: dict, restricted_locals: dict, *args_list: list) -> dict:

        if self.__compile_result.code is None:  # in case it's 'None', but should never become true.
            return self.__sandbox_logs

        try:
            # Run code
            exec(self.__compile_result.code, restricted_globals, restricted_locals)

        except TimeoutError:
            # code execution took too long
            import traceback

            self.__sandbox_logs["EXECUTELOG"]["ERROR"] = \
                f'TimeoutError: Code execution has been interrupted. Maximum execution time has been reached!'
            return self.__sandbox_logs

        except:
            # The code did something that is not allowed. Runtime error in code.
            import traceback
            type_, value_, traceback_ = sys.exc_info()

            self.__sandbox_logs["EXECUTELOG"]["ERROR"] = value_
            return self.__sandbox_logs

        else:
            for idx, arg in enumerate(args_list):
                self.__sandbox_logs["RESULTLOG"][f'{idx}'] = (arg, [restricted_locals["result"][idx]])

            return self.__sandbox_logs
