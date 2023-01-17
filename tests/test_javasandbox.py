#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Kev.in - a coding learning platform
# Copyright (C) 2022  Max Linke
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

import unittest
import requests
from parameterized import parameterized

# This unit test is written in pseudocode as the class ExecuteJava isn't deployed yet.
# The unit test is similarly structured to the unit test in test_pysandbox.py,
# that tests the class ExecutePython.
# The main difference between both sandboxes is, that we need to set up a socket in ExecuteJava class,
# which is done with the Py4J API. This socket allows us to connect to the Java Virtual Machine (JVM) and
# call any method defined on the Java side in Python.
# Before we can access the Java side, we create a subprocess,
# which creates a Gateway on the Java side from a Java-file called SandboxEntryPoint and
# afterwards we will create a Gateway in Python. With the set upped connection to the JVM
# we can access our Java sandbox class and push the untrusted user code to the corresponding member function.
# The member function of the Java sandbox class will execute the untrusted user code and
# give feedback to the Python backend. Subsequently, the ExecuteJava class will kill the subprocess,
# that executes the mentioned Java-file, and return the result to the Evaluator class.


class JavaSandboxTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # TODO: is a setup needed?
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        # TODO: is a tear down needed?
        pass

    def test_init_constructor(self) -> None:
        """Tests correct initialization of an instance of the ExecuteJava class."""
        pass

    def test_jvm_connection(self) -> None:
        """Test whether JVM connection is present."""
        pass

    @parameterized.expand([["hello"], ["world"]])
    def test_correct_user_code(self, test_input) -> None:
        """Tests correct user code. There are no syntax, compilation or runtime errors and the code works as intended."""
        pass

    @parameterized.expand([["hello"], ["world"]])
    def test_wrong_user_code(self, test_input) -> None:
        """Tests wrong user code. There are no errors, but the code does not work as intended."""
        pass

    @parameterized.expand([["infinite loop"]])
    def test_timeout(self, test_input) -> None:
        """Tests long running user code. Long running user code should be catched by a timeout handler."""
        pass

    @parameterized.expand([["error code"]])
    def test_not_compilable(self, test_input) -> None:
        """Tests system behavior when user code results in a syntax or compilation error."""
        pass

    @parameterized.expand([["runtime error"]])
    def test_not_executable(self, test_input) -> None:
        """Tests system behavior when user code encounters a runtime error."""
        pass


if __name__ == "__main__":
    unittest.main()
