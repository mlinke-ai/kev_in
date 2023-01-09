#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest


class EvaluatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_python_sandbox(self) -> None:
        pass

    def test_java_sandbox(self) -> None:
        pass


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
