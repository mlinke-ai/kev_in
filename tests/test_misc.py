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
from flask_unittest.case import FlaskClient

from backend import create_app


class MiscTest(flask_unittest.ClientTestCase):
    app = create_app()

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self, client: FlaskClient) -> None:
        pass

    def tearDown(self, client: FlaskClient) -> None:
        pass

    def test_missing_route_code(self, client: FlaskClient) -> None:
        r = client.get("/missing-route")
        self.assertEqual(r.status_code, 404)

    def test_user_route_code(self, client: FlaskClient) -> None:
        r = client.get("/user")
        self.assertNotEqual(r.status_code, 404)

    def test_exercise_route_code(self, client: FlaskClient) -> None:
        r = client.get("/exercise")
        self.assertNotEqual(r.status_code, 404)

    def test_solution_route_code(self, client: FlaskClient) -> None:
        r = client.get("/solution")
        self.assertNotEqual(r.status_code, 404)

    def test_login_route_code(self, client: FlaskClient) -> None:
        r = client.post("/login")
        self.assertNotEqual(r.status_code, 404)

    def test_logout_route_code(self, client: FlaskClient) -> None:
        r = client.delete("/logout")
        self.assertNotEqual(r.status_code, 404)


if __name__ == "__main__":
    flask_unittest.main()
