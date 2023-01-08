#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from flask import Response, jsonify, make_response
from flask_restful import Resource, reqparse
from backend.lib.sandbox.pyenv.pysandbox import ExecutePython

# TODO:
# Unit test
# - Evaluator class (pseudocode)
# - PythonSandbox class
# - JavaSandbox class (pseudocode)

# webResponse = requests.post(
#     "http://127.0.0.1:5000/",
#     json={"exercise_id": "1",
#           "user_result": "def fib(n):\
#     # Check if input is 0 then it will\
#     # print incorrect input\
#     if n < 0:\
#         return\
#     # Check if n is 0\
#     # then it will return 0\
#     elif n == 0:\
#         return 0\
#     # Check if n is 1,2\
#     # it will return 1\
#     elif n == 1 or n == 2:\
#         return 1\
#     else:\
#         return fib(n - 1) + fib(n - 2)"},
#     headers={"Content-Type": "application/json"},
# )

class EvaluatorResource(Resource):
    pass

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
#
#
# class TestClass:
#
#     def __init__(self, user_func):
#         self.user_func = user_func
#         self.test_args = None
#         self.input_data = dict()
#
#     def generate_input_data(self):
#         if self.user_func == "fib":
#             # fibonacci
#             self.input_data["0"] = ([0], [0])
#             self.input_data["1"] = ([1], [1])
#             self.input_data["2"] = ([7], [13])
#         elif self.user_func == "reverse_for_loop":
#             # reverseStringLoop
#             self.input_data = dict()
#             self.input_data["0"] = (['"Hello World"'], ['dlroW olleH'])
#             self.input_data["1"] = (['"Kev.in"'], ['ni.veK'])
#         elif self.user_func == "multiplicate":
#             # multiplication
#             self.input_data = dict()
#             self.input_data["0"] = ([2, 2, 2], [8])
#         else:
#             return
#
#         self.test_args = [args[0] for args in self.input_data.values()]
