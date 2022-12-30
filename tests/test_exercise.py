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


class ExerciseTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        #log into sadmin
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_name": "sadmin", "user_pass": "sadmin"},
            headers={"Content-Type": "application/json"},
        )
        cls.cookie = r.headers["Set-Cookie"]

    @classmethod
    def tearDownClass(cls) -> None:
        #log out of sadmin
        
        cls.cookie = ""

    def test_get_existing(self) -> None:

        id = "1"
        r = requests.request(
            "GET", f"http://127.0.0.1:5000/exercise?exercise_id={id}",
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
            )
        self.assertEqual(r.status_code, 200)
        try:
            exercise = r.json()[id]
        except KeyError:
            self.fail("An exercise should be returned")
        
        #returned exercise should have these attributes
        self.assertIn("exercise_content", exercise)
        self.assertIn("exercise_description", exercise)
        self.assertIn("exercise_id", exercise)
        self.assertIn("exercise_title", exercise)
        self.assertIn("exercise_type", exercise)
        
    def test_get_non_existing(self) -> None:
        r = requests.request(
            "GET", "http://127.0.0.1:5000/exercise?exercise_id=-2",
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {})
        
if __name__ == "__main__":
    unittest.main()