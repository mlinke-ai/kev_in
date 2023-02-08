#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .sandboxes.pyenv.pysandbox import ExecutePython


# from .sandboxes.javaenv.javasandbox import ExecuteJava

class Evaluator:

    # TODO
    @staticmethod
    def evaluate(**kwargs):
        # Define input arguments for evaluate
        # Get user func from head e.g. "def func(someArg, ...,)->None:" -> "func"
        pass

    # TODO function name required "user_func"
    @staticmethod
    def evaluate_user_code(user_code: str, user_func: str, language: str, **args_result_dict: dict) -> dict:
        """
        Description: Execute and evaluate untrusted user code.

        Args:
            user_code: String containing user code.
            user_func: Function inside user_code to execute.
            language: "python" or "java"
            **args_result_dict: Dictionary {'1': ([Arg1, Arg2,.., Argsn], [Result]), \
                                            '2': ([Args], [Result]), ..}
                                            e.g. {"0": ([2, 2, 2], [8])}
                                            Dictionary with input args and expected result.
        Return:
            Dictonary as a result log:
            {'Correct': ""} or if false
            {'Incorrect': "E.g. some errors, exceptions, or wrong result information"}
        """
        if language == "python":
            pySandbox = ExecutePython()
            arg_list = [args[0] for args in args_result_dict.values()]
            result_log = pySandbox.exec_untrusted_code(user_code, user_func, *arg_list)

            if result_log['RESULTLOG']:
                # successful execution of user code
                if result_log['RESULTLOG'] == args_result_dict:
                    # user code correct
                    return {'Correct': ""}
                else:
                    # user code not correct
                    return {'Incorrect': "Expected results do not equal results."}

            # Errors, Exceptions when executing user code
            else:
                if len(result_log['COMPILERLOG']['ERROR']) != 0:
                    # interpreter error
                    return {'False': result_log['COMPILERLOG']['ERROR']}
                else:
                    # execution error
                    return {'False': result_log['EXECUTELOG']['ERROR']}

        elif language == "java":
            return {'Incorrect': "Not implemented yet"}
        else:
            return dict()
