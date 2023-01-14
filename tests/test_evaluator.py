#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from parameterized import parameterized
from backend.lib.evaluator import Evaluator

# Calculate fibonacci with recursion in Python (Correct program).
fibonacci_py = {
    "user_code": "def fib(n):\r\n\r\n    # Check if input is 0 then it will\r\n    # print incorrect input\r\n    if "
                 "n < 0:\r\n        return\r\n\r\n    # Check if n is 0\r\n    # then it will return 0\r\n    elif n "
                 "== 0:\r\n        return 0\r\n\r\n    # Check if n is 1,2\r\n    # it will return 1\r\n    elif n == "
                 "1 or n == 2:\r\n        return 1\r\n\r\n    else:\r\n        return fib(n - 1) + fib(n - 2)",
    "user_func": "fib",
    "language": "python",
    "args_result": {"0": ([0], [0]), "1": ([1], [1]), "2": ([7], [13])},
    "expected": "Correct",
}

# Calculate fibonacci with recursion in Java (Correct program).
fibonacci_java = {
    "user_code": "public int fib(int n)  {\r\n    if(n == 0)\r\n        return 0;\r\n    else if(n == 1)\r\n    "
                 "  return 1;\r\n   else\r\n      return fib(n - 1) + fib(n - 2);\r\n}",
    "user_func": "fib",
    "language": "java",
    "args_result": {"0": ([0], [0]), "1": ([1], [1]), "2": ([7], [13])},
    "expected": "Correct",
}

# Calculate fibonacci with recursion in Python (Incorrect program).
fibonacci_py_wrong = {
    "user_code": "def fib(n):\r\n\r\n    # Check if input is 0 then it will\r\n    # print incorrect input\r\n    if "
                 "n < 0:\r\n        return\r\n\r\n    # Check if n is 0\r\n    # then it will return 0\r\n    elif n "
                 "== 0:\r\n        return 0\r\n\r\n    # Check if n is 1,2\r\n    # it will return 1\r\n    elif n == "
                 "1 or n == 2:\r\n        return 1\r\n\r\n    else:\r\n        return fib(n - 1)",
    "user_func": "fib",
    "language": "python",
    "args_result": {"0": ([0], [0]), "1": ([1], [1]), "2": ([7], [13])},
    "expected": "Incorrect",
}

# Calculate fibonacci with recursion in Java (Incorrect program).
fibonacci_java_wrong = {
    "user_code": "public int fib(int n)  {\r\n    if(n == 0)\r\n        return 0;\r\n    else if(n == 1)\r\n    "
                 "  return 1;\r\n   else\r\n      return fib(n - 1);\r\n}",
    "user_func": "fib",
    "language": "java",
    "args_result": {"0": ([0], [0]), "1": ([1], [1]), "2": ([7], [13])},
    "expected": "Incorrect",
}


class EvaluatorTest(unittest.TestCase):

    @parameterized.expand([[fibonacci_py], [fibonacci_py_wrong], [fibonacci_java], [fibonacci_java_wrong]])
    def test_evaluate_python_sandbox(self, input_data) -> None:
        """"" 
        Test checks if evaluation of the user code is handled in correct way.
        Example of "input_data" are given at the beginning of the file (e.g. 
        fibonacci_py). "parameterized" allows us to run the test for 
        multiple "input_data".
        For more information see @https://github.com/wolever/parameterized
        The inputs are various user code implementations in Java or Python.
        It is checked if the evaluator treats incorrect user code as "incorrect" 
        and correct user code as "correct".
        """""
        user_code = input_data['user_code']
        user_func = input_data['user_func']
        language = input_data['language']
        args_result = input_data['args_result']
        expected = input_data['expected']

        result = dict()
        result = Evaluator.evaluate_user_code(user_code, user_func, language, **args_result)
        self.assertIsNot(result, None)
        self.assertEqual(list(result.keys())[0], expected)


if __name__ == "__main__":
    unittest.main()
