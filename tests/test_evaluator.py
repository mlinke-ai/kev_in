#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from parameterized import parameterized

from backend.lib.evaluator import Evaluator

# TEST CASES EVALUATE GAP TEXT START
gt_correct = {
    "solution_content":
        {"gap_entries": ["a", "b", "c"]},
    "exercise_solution":
        {"gap_entries": ["a", "b", "c"]},
    "expected": (True, 'Correctly filled all gaps')
}

gt_wrong = {
    "solution_content":
        {"gap_entries": ["a", "b", "c"]},
    "exercise_solution":
        {"gap_entries": ["a", "no clue", "c"]},
    "expected": (False, 'Some gaps were not correctly filled')
}

# TEST CASES EVALUATE GAP TEXT END
#
# TEST CASES EVALUATE PARSONS PUZZLE START
pp_correct = {
    "solution_content":
        {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
    "exercise_solution":
        {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
    "expected": (True, 'Correctly ordered all pieces')
}

pp_wrong = {
    "solution_content":
        {"list": ["World", "Hello", "this", "is", "the", "first", "exercise"]},
    "exercise_solution":
        {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
    "expected": (False, 'Wrong order of pieces')
}

# TEST CASES EVALUATE PARSONS PUZZLE END
#
# TEST CASES EVALUATE USER CODE START

# Calculate fibonacci with recursion in Python (Correct program).
fibonacci_py = {
    "solution_content":
        {"code": "def fib(n):\r\n\r\n    # Check if input is 0 then it will\r\n    # print incorrect input\r\n    if "
                 "n < 0:\r\n        return\r\n\r\n    # Check if n is 0\r\n    # then it will return 0\r\n    elif n "
                 "== 0:\r\n        return 0\r\n\r\n    # Check if n is 1,2\r\n    # it will return 1\r\n    elif n == "
                 "1 or n == 2:\r\n        return 1\r\n\r\n    else:\r\n        return fib(n - 1) + fib(n - 2)"},
    "function_head": "fib",
    "language": "Python",
    "exercise_solution": {"0": [[0], [0]], "1": [[1], [1]], "2": [[7], [13]]},
    "expected": (True, 'Successfully passed all Tests')
}

# Calculate fibonacci with recursion in Java (Correct program).
fibonacci_java = {
    "solution_content":
        {"code": "public int fib(int n)  {\r\n    if(n == 0)\r\n        return 0;\r\n    else if(n == 1)\r\n    "
                 "  return 1;\r\n   else\r\n      return fib(n - 1) + fib(n - 2);\r\n}"},
    "function_head": "fib",
    "language": "Java",
    "exercise_solution": {"0": ([0], [0]), "1": ([1], [1]), "2": ([7], [13])},
    "expected": (True, 'Successfully passed all Tests')
}

# Calculate fibonacci with recursion in Python (Incorrect program).
fibonacci_py_wrong = {
    "solution_content": {
        "code": "def fib(n):\r\n\r\n    # Check if input is 0 then it will\r\n    # print incorrect input\r\n    if "
                "n < 0:\r\n        return\r\n\r\n    # Check if n is 0\r\n    # then it will return 0\r\n    elif n "
                "== 0:\r\n        return 0\r\n\r\n    # Check if n is 1,2\r\n    # it will return 1\r\n    elif n == "
                "1 or n == 2:\r\n        return 1\r\n\r\n    else:\r\n        return fib(n - 1)"},
    "function_head": "fib",
    "language": "Python",
    "exercise_solution": {"0": ([0], [0]), "1": ([1], [1]), "2": ([7], [13])},
    "expected": (False, 'Some Test cases failed')
}

# Calculate fibonacci with recursion in Java (Incorrect program).
fibonacci_java_wrong = {
    "solution_content": {
        "code": "public int fib(int n)  {\r\n    if(n == 0)\r\n        return 0;\r\n    else if(n == 1)\r\n    "
                "  return 1;\r\n   else\r\n      return fib(n - 1);\r\n}"},
    "function_head": "fib",
    "language": "Java",
    "exercise_solution": {"0": ([0], [0]), "1": ([1], [1]), "2": ([7], [13])},
    "expected": (False, "Some Tests failed.")
}


# TEST CASES EVALUATE USER CODE END

class EvaluatorTest(unittest.TestCase):
    @parameterized.expand([[gt_correct], [gt_wrong]])
    def test_evaluate_gap_text(self, input_data) -> None:
        """Tests whether solutions for gap text exercises get correctly evaluated"""
        user_input = input_data["solution_content"]
        exercise_solution = input_data["exercise_solution"]
        expected = input_data["expected"]

        result = Evaluator.evaluate_gap_text(user_input, exercise_solution)

        self.assertIsNot(result, None)
        self.assertEqual(result, expected)

    def test_evaluate_syntax(self) -> None:
        """Tests whether solutions for syntax error exercises get correctly evaluated"""
        pass

    @parameterized.expand([[pp_correct], [pp_wrong]])
    def test_evaluate_ppe(self, input_data) -> None:
        """Tests whether solutions for parsons puzzle exercises get correctly evaluated"""
        user_input = input_data["solution_content"]
        exercise_solution = input_data["exercise_solution"]
        expected = input_data["expected"]

        result = Evaluator.evaluate_ppe(user_input, exercise_solution)

        self.assertIsNot(result, None)
        self.assertEqual(result, expected)

    def test_evaluate_find_the_bug(self) -> None:
        """Tests whether solutions for find the bug exercises get correctly evaluated"""
        pass

    def test_evaluate_documentation(self) -> None:
        """Tests whether solutions for documentation exercises get correctly evaluated"""
        pass

    def test_evaluate_output(self) -> None:
        """Tests whether solutions for output exercises get correctly evaluated"""
        pass

    @parameterized.expand([[fibonacci_py], [fibonacci_py_wrong], [fibonacci_java], [fibonacci_java_wrong]])
    def test_evaluate_user_code(self, input_data) -> None:
        """
        Test checks if evaluation of the user code is handled in correct way.
        Example of "input_data" are given at the beginning of the file (e.g.
        fibonacci_py). "parameterized" allows us to run the test for
        multiple "input_data".
        For more information see @https://github.com/wolever/parameterized
        The inputs are various user code implementations in Java or Python.
        It is checked if the evaluator treats incorrect user code as "incorrect"
        and correct user code as "correct".
        """
        user_code = input_data["solution_content"]
        user_func = input_data["function_head"]
        language = input_data["language"]
        exercise_solution = input_data["exercise_solution"]
        expected = input_data["expected"]

        if language == "Java":
            return  # TODO: IMPLEMENT JAVA SANDBOX

        result = Evaluator.evaluate_user_code(user_code, language, exercise_solution, user_func)
        self.assertIsNot(result, None)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
