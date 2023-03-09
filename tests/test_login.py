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

import flask_unittest
from flask_sqlalchemy.query import sqlalchemy
from flask_unittest import ClientTestCase
from flask_unittest.case import FlaskClient, unittest
from parameterized import parameterized

from backend import create_app
from backend.database.models import UserModel, UserRole, db


class BaseTest(ClientTestCase):
    app = create_app("testing.cfg")
    base_header = {"Content-Type": "application/json"}

    def setUp(self, client: FlaskClient) -> None:
        raise NotImplementedError

    def tearDown(self, client: FlaskClient) -> None:
        raise NotImplementedError


@unittest.skip("Work in progress")
class LoginTest(BaseTest):
    """
    This test class tests everything related to the login process over HTTP.
    The documentation of the API can be found [here](https://mlinke-ai.github.io/kev_in/api/login/).
    """

    user_mail = "sadmin@example.com"
    user_pass = "sadmin"
    user_name = "sadmin"

    def test_login_success(self, client: FlaskClient) -> None:
        """
        Log in the existing sadmin account with right username and password.
        The system should return HTTP-status 200, a response message and a Session-Cookie.
        """

        r = client.post(
            "/login",
            json={"user_mail": LoginTest.user_mail, "user_pass": LoginTest.user_pass},
            headers={"Content-Type": "application/json"},
        )

        self.assertIn("Set-Cookie", r.headers)  # cookie with JWT should be returned
        self.assertDictEqual(
            {
                "message": f"Welcome {LoginTest.user_name}!",
                "user_id": 1,
                "user_mail": "sadmin@example.com",
                "user_name": "sadmin",
                "user_role_name": "SAdmin",
                "user_role_value": 1,
            },
            r.json,
        )
        self.assertEqual(200, r.status_code)
        self.assertTrue(r.is_json)

    def test_login_fail(self, client: FlaskClient) -> None:
        """
        Log in the existing sadmin account with wrong password.
        The system should return HTTP-status 401, a fail message and no Session-Cookie.
        """

        r = client.post(
            "/login",
            json={"user_mail": "unkownUser@example.com", "user_pass": LoginTest.user_pass},
            headers={"Content-Type": "application/json"},
        )

        self.assertNotIn("Set-Cookie", r.headers)  # no cookie should be returned
        self.assertDictEqual({"message": "Incorrect user name or password"}, r.json)
        self.assertEqual(r.status_code, 401)
        self.assertTrue(r.is_json)

        r = client.post(
            "/login",
            json={"user_mail": LoginTest.user_mail, "user_pass": "trashPW"},
            headers={"Content-Type": "application/json"},
        )

        self.assertNotIn("Set-Cookie", r.headers)  # no cookie should be returned
        self.assertDictEqual({"message": "Incorrect user name or password"}, r.json)
        self.assertEqual(r.status_code, 401)
        self.assertTrue(r.is_json)

    def test_login_without_req_arg(self, client: FlaskClient) -> None:
        """
        Try to log in an sadmin account without giving required argument user_mail and user_pass.
        The system should respond with an error message about the missing argument in JSON,
        HTTP-status 400 and without a Session-Cookie.
        """

        r = client.post(
            "/login",
            json={"user_pass": LoginTest.user_pass},
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        try:
            errors = r.json["message"]
        except KeyError:
            self.fail("An error message should be returned")

        self.assertNotIn("Set-Cookie", r.headers)  # no cookie should be returned
        self.assertIn("user_mail", errors)

        r = client.post(
            "/login",
            json={"user_mail": LoginTest.user_mail},
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        try:
            errors = r.json["message"]
        except KeyError:
            self.fail("An error message should be returned")

        self.assertNotIn("Set-Cookie", r.headers)  # no cookie should be returned
        self.assertIn("user_pass", errors)


if __name__ == "__main__":
    flask_unittest.main()
