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


class SolutionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    # --- GET ---

    def test_get_existing_by_id(self) -> None:
        pass

    def test_get_existing_by_user_id(self) -> None:
        pass

    def test_get_existing_by_exercise_id(self) -> None:
        pass

    def test_get_existing_by_date(self) -> None:
        pass

    def test_get_existing_by_duration(self) -> None:
        pass

    def test_get_existing_by_correct(self) -> None:
        pass

    def test_get_existing_by_pending(self) -> None:
        pass

    def test_get_non_existing_by_id(self) -> None:
        pass

    def test_get_non_existing_by_user_id(self) -> None:
        pass

    def test_get_non_existing_by_exercise_id(self) -> None:
        pass

    def test_get_non_existing_by_date(self) -> None:
        pass

    def test_get_non_existing_by_duration(self) -> None:
        pass

    def test_get_non_existing_by_correct(self) -> None:
        pass

    def test_get_non_existing_by_pending(self) -> None:
        pass

    def test_get_restrict_page_size(self) -> None:
        pass

    # --- POST ---

    def test_create_as_user(self) -> None:
        pass

    def test_create_as_admin(self) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "sadmin@example.com", "user_pass": "sadmin"},
            headers={"Content-Type": "application/json"},
        )
        c = r.headers["Set-Cookie"]
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={"solution_exercise": 1, "solution_date": 1674501941, "solution_duration": 128},
            headers={"Content-Type": "application/json", "Cookies": c},
        )
        print(r.json())

    def test_create_without_token(self) -> None:
        pass

    def test_create_without_user_id(self) -> None:
        pass

    def test_create_without_exercise_id(self) -> None:
        pass

    def test_create_with_date_in_past(self) -> None:
        pass

    def test_create_with_negative_duration(self) -> None:
        pass

    def test_create_with_empty_text(self) -> None:
        pass

    def test_create_with_malformed_text(self) -> None:
        pass

    # --- PUT ---

    def test_change_existing(self) -> None:
        pass

    def test_change_non_existing(self) -> None:
        pass

    def test_change_as_user(self) -> None:
        pass

    def test_change_as_admin(self) -> None:
        pass

    def test_change_without_token(self) -> None:
        pass

    def test_change_to_empty_user(self) -> None:
        pass

    def test_change_to_empty_exercise(self) -> None:
        pass

    def test_change_to_date_in_past(self) -> None:
        pass

    def test_change_to_negative_duration(self) -> None:
        pass

    def test_change_to_empty_text(self) -> None:
        pass

    def test_change_to_malformed_text(self) -> None:
        pass

    # --- DELETE ---

    def test_delete_existing(self) -> None:
        pass

    def test_delete_non_existing(self) -> None:
        pass

    def test_delete_as_user(self) -> None:
        pass

    def test_delete_as_admin(self) -> None:
        pass

    def test_delete_without_token(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
