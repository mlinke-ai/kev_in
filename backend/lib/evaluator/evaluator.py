#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sandboxes.pyenv.pysandbox import ExecutePython
from sandboxes.javaenv.javasandbox import ExecuteJava


class Evaluator:
    @classmethod
    def execute(cls, code, language):
        # TODO: add execution of code
        # execute code inside the language respective sandbox
        pass

    @classmethod
    def evaluate(cls, exercise, solution):
        # TODO: add evaluation of solution
        # evaluate a solution against a an exercise
        pass


# TODO: we won't need this code, API calls are handled by the Solution endpoint
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('exercise_id', type=str, required=True)
#         parser.add_argument('user_result', type=list(), required=True)
#
#         exercise_id = parser.parse_args().get('exercise_id')
#
#         # TODO:
#         """ Decide on the basis of exercise_id which exercise type and how the evaluation
#         must take place. Ask our database for "category", "user_func" (if present), "test_args", "solution" """
#
#         """" python evaluator """""
#         user_code = parser.parse_args().get('user_result')
#
#         # user_func = "multiplicate"
#         user_func = "fib"
#         # user_func = "reverse_for_loop"
#
#         myTest = TestClass(user_func)
#         myTest.generate_input_data()
#         pythonEvaluator = ExecutePython()
#         sandbox_log = pythonEvaluator.exec_untrusted_code(user_code=user_code, user_func=user_func, *myTest.test_args)
#
#         response = dict()
#         if not sandbox_log["RESULTLOG"]:
#             # execute user code failed
#             if sandbox_log["EXECUTELOG"]:
#                 # execution error
#                 response["Execution Error"] = sandbox_log.get("EXECUTELOG")
#             else:
#                 # interpreter error
#                 response["Interpreter Error"] = sandbox_log.get("COMPILERLOG")
#             return make_response(jsonify(response), 200)
#
#         if sandbox_log["RESULTLOG"] == myTest.input_data:
#             # successful
#             response["Result Correct"] = sandbox_log.get("RESULTLOG")
#         else:
#             response["RESULT False"] = sandbox_log.get("RESULTLOG")
#
#         return make_response(jsonify(response), 200)
