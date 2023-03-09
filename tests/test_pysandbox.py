#!/usr/bin/python3
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

import flask_unittest
from flask_unittest import ClientTestCase
from flask_unittest.case import FlaskClient, unittest
from parameterized import parameterized

from backend import create_app
from backend.evaluator.evaluator import ExecutePython

# Test input parameter

# Correct user code.
# Calculate fibonacci with recursion.
fibonacci = {
    "user_code": "def fib(n):\r\n\r\n    # Check if input is 0 then it will\r\n    # print incorrect input\r\n    if "
    "n < 0:\r\n        return\r\n\r\n    # Check if n is 0\r\n    # then it will return 0\r\n    elif n "
    "== 0:\r\n        return 0\r\n\r\n    # Check if n is 1,2\r\n    # it will return 1\r\n    elif n == "
    "1 or n == 2:\r\n        return 1\r\n\r\n    else:\r\n        return fib(n - 1) + fib(n - 2)",
    "user_func": "fib",
    "test_args": [[0], [1], [7]],
    "expected": {
        "COMPILERLOG": {"ERROR": (), "WARNINGS": []},
        "EXECUTELOG": {"ERROR": ()},
        "RESULTLOG": {"0": [[0], [0]], "1": [[1], [1]], "2": [[7], [13]]},
    },
}

# Reverse String with loop.
reverse_string = {
    "user_code": "def reverseString(s):\r\n    s1 = ''\r\n    for c in s:\r\n        s1 = c + s1  # appending chars "
    "in reverse order\r\n    return s1",
    "user_func": "reverseString",
    "test_args": [['"Hello World"'], ['"Kev.in"']],
    "expected": {
        "COMPILERLOG": {"ERROR": (), "WARNINGS": []},
        "EXECUTELOG": {"ERROR": ()},
        "RESULTLOG": {
            "0": [['"Hello World"'], ["dlroW olleH"]],
            "1": [['"Kev.in"'], ["ni.veK"]],
        },
    },
}

# Multiplication with three input parameter.
multiplication = {
    "user_code": "def mult(a, b, c):\r\n    return a*b*c",
    "user_func": "mult",
    "test_args": [[2, 2, 2]],
    "expected": {
        "COMPILERLOG": {"ERROR": (), "WARNINGS": []},
        "EXECUTELOG": {"ERROR": ()},
        "RESULTLOG": {"0": [[2, 2, 2], [8]]},
    },
}

# Wrong user code.
# Multiplication with three input parameter.
multiplication_wrong = {
    "user_code": "def mult(a, b, c):\r\n    return a*c",
    "user_func": "mult",
    "test_args": [[2, 2, 2]],
    "not_expected": {
        "COMPILERLOG": {"ERROR": (), "WARNINGS": []},
        "EXECUTELOG": {"ERROR": ()},
        "RESULTLOG": {"0": [[2, 2, 2], [8]]},
    },
}

# Calculate fibonacci with recursion.
fibonacci_wrong = {
    "user_code": "def fib(n):\r\n\r\n    # Check if input is 0 then it will\r\n    # print incorrect input\r\n    if "
    "n < 0:\r\n        return\r\n\r\n    # Check if n is 0\r\n    # then it will return 0\r\n    elif n "
    "== 0:\r\n        return 0\r\n\r\n    # Check if n is 1,2\r\n    # it will return 1\r\n    elif n == "
    "1 or n == 2:\r\n        return 1\r\n\r\n    else:\r\n        return fib(n - 1)",
    "user_func": "fib",
    "test_args": [[0], [1], [7]],
    "not_expected": {
        "COMPILERLOG": {"ERROR": (), "WARNINGS": []},
        "EXECUTELOG": {"ERROR": ()},
        "RESULTLOG": {"0": [[0], [0]], "1": [[1], [1]], "2": [[7], [13]]},
    },
}

# Infinite loop
infinite_loop = {
    "user_code": "def infinite_loop(s):\r\n    while 1:\r\n        pass",
    "user_func": "infinite_loop",
    "test_args": [['"Hello World"']],
    "expected": {
        "COMPILERLOG": {"ERROR": (), "WARNINGS": []},
        "EXECUTELOG": {
            "ERROR": ("TimeoutError: Code execution has been interrupted. Maximum execution time " "has been reached!",)
        },
        "RESULTLOG": {},
    },
}

# Not compilable. Here SyntaxError -> after while ":" missing
not_compilable = {
    "user_code": "def not_compilable(s):\r\n    while 1\r\n        pass",
    "user_func": "not_compilable",
    "test_args": [['"Hello World"']],
}

# Not executable. Here ImportError -> "import os"
not_executable = {
    "user_code": "import os\r\ndef not_executable(s):\r\n    s1 = ''\r\n    for c in s:\r\n        s1 = c + s1  # "
    "appending chars in reverse order\r\n    return s1",
    "user_func": "not_executable",
    "test_args": [['"Hello World"']],
    "expected": {"COMPILERLOG": {"ERROR": (), "WARNINGS": []}, "RESULTLOG": {}},
}

# Create test case


class BaseTest(ClientTestCase):
    app = create_app("testing.cfg")
    base_header = {"Content-Type": "application/json"}

    def setUp(self, client: FlaskClient) -> None:
        raise NotImplementedError

    def tearDown(self, client: FlaskClient) -> None:
        raise NotImplementedError


@unittest.skip("Work in progress")
class TestPySandbox(BaseTest):
    # Automatically call for every single test we run.
    def setUp(self):
        self.pysandbox_instance = ExecutePython()

    def test_init_constructor(self):
        """Tests correct initialization of an instance of the ExecutePython class"""
        self.assertIsNotNone(self.pysandbox_instance)

    # Test input
    @parameterized.expand([[fibonacci], [reverse_string], [multiplication]])
    def test_correct_user_code(self, test_input: list) -> None:
        """Tests user code which is correct. So all expected results are met."""
        user_code = test_input["user_code"]
        user_func = test_input["user_func"]
        test_args = test_input["test_args"]
        expected = test_input["expected"]
        self.assertEqual(
            self.pysandbox_instance.exec_untrusted_code(user_code, user_func, *test_args),
            expected,
        )

    # Test input
    @parameterized.expand([[multiplication_wrong], [fibonacci_wrong]])
    def test_wrong_user_code(self, test_input: list) -> None:
        """Tests user code which is wrong. So at least one expected result is not met."""
        user_code = test_input["user_code"]
        user_func = test_input["user_func"]
        test_args = test_input["test_args"]
        not_expected = test_input["not_expected"]
        self.assertNotEqual(
            self.pysandbox_instance.exec_untrusted_code(user_code, user_func, *test_args),
            not_expected,
        )

    # Test input
    @parameterized.expand([[infinite_loop]])
    def test_timeout(self, test_input: list) -> None:
        """Tests long execution time in user code. For example an infinite loop should result in a TimeoutError."""
        user_code = test_input["user_code"]
        user_func = test_input["user_func"]
        test_args = test_input["test_args"]
        expected = test_input["expected"]
        self.assertEqual(
            self.pysandbox_instance.exec_untrusted_code(user_code, user_func, *test_args),
            expected,
        )

    # Test input
    @parameterized.expand([[not_compilable]])
    def test_not_compilable(self, test_input: list) -> None:
        """Tests user code is not compilable -> COMPILER ERROR. For example SyntaxError."""
        user_code = test_input["user_code"]
        user_func = test_input["user_func"]
        test_args = test_input["test_args"]
        result = self.pysandbox_instance.exec_untrusted_code(user_code, user_func, *test_args)
        self.assertIsNot(len(result["COMPILERLOG"]["ERROR"]), 0)

    # Test input
    @parameterized.expand([[not_executable]])
    def test_not_executable(self, test_input: list) -> None:
        """Tests user code is not executable -> EXECUTE ERROR. For example ImportError."""
        user_code = test_input["user_code"]
        user_func = test_input["user_func"]
        test_args = test_input["test_args"]
        result = self.pysandbox_instance.exec_untrusted_code(user_code, user_func, *test_args)
        self.assertIsNot(len(result["EXECUTELOG"]["ERROR"]), 0)


if __name__ == "__main__":
    flask_unittest.main()
