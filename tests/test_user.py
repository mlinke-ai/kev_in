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


class UserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_name": "sadmin", "user_pass": "sadmin"},
            headers={"Content-Type": "application/json"},
        )
        cls.token = r.json()["token"]

    @classmethod
    def tearDownClass(cls) -> None:
        # TODO: implement test user logout
        pass

    def test_get_existing(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user",
            json={"user_name": "sadmin"},
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {UserTest.token}"},
        )
        # print(r.status_code, r.json())
        self.assertEqual(r.status_code, 200)

    def test_get_non_existing(self) -> None:
        r = requests.request(
            "GET",
            "http://127.0.0.1:5000/user",
            json={"user_name": "This user does not exist"},
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {UserTest.token}"},
        )
        # print(r.status_code, r.json())
        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()
