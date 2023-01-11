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


class LoginTest(unittest.TestCase):
    """
    This test class tests everything related to the login process over HTTP.
    The documentation of the API can be found [here](https://mlinke-ai.github.io/kev_in/api/login/).
    """
    user_name = "sadmin"
    user_pass = "sadmin"

    def test_login_success(self) -> None:
        """
        Log in the existing sadmin account with right username and password.
        The system should return HTTP-status 200, a response message and a Session-Cookie.
        """

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_name": LoginTest.user_name, "user_pass": LoginTest.user_pass},
            headers={"Content-Type": "application/json"},
        )

        self.assertIn("Set-Cookie", r.headers) #cookie with JWT should be returned
        self.assertDictEqual({"message": f"Welcome {LoginTest.user_name}!"}, r.json())
        self.assertEqual(200, r.status_code)

    def test_login_fail(self) -> None:
        """
        Log in the existing sadmin account with wrong password.
        The system should return HTTP-status 401, a fail message and no Session-Cookie.
        """

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_name": "unkownUser", "user_pass": LoginTest.user_pass},
            headers={"Content-Type": "application/json"},
        )

        self.assertNotIn("Set-Cookie", r.headers) #no cookie should be returned
        self.assertDictEqual({"message": "Incorrect user name or password"}, r.json())
        self.assertEqual(r.status_code, 401)

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_name": LoginTest.user_name, "user_pass": "trashPW"},
            headers={"Content-Type": "application/json"},
        ) 

        self.assertNotIn("Set-Cookie", r.headers) #no cookie should be returned
        self.assertDictEqual({"message": "Incorrect user name or password"}, r.json())
        self.assertEqual(r.status_code, 401)

    def test_login_without_req_arg(self) -> None:
        """
        Try to log in an sadmin account without giving required argument user_name and user_pass.
        The system should respond with an error message about the missing argument in JSON,
        HTTP-status 400 and without a Session-Cookie.
        """

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_pass": LoginTest.user_pass},
            headers={"Content-Type": "application/json"},
        )

        try:
            errors = r.json()["message"]
        except KeyError:
            self.fail("An error message should be returned")

        self.assertNotIn("Set-Cookie", r.headers) #no cookie should be returned
        self.assertIn("user_name", errors)
        self.assertEqual(r.status_code, 400)

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_name": LoginTest.user_name},
            headers={"Content-Type": "application/json"},
        )

        try:
            errors = r.json()["message"]
        except KeyError:
            self.fail("An error message should be returned")

        self.assertNotIn("Set-Cookie", r.headers) #no cookie should be returned
        self.assertIn("user_pass", errors)
        self.assertEqual(r.status_code, 400)