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

    def setUp(self, client: FlaskClient) -> None:
        pass

    def tearDown(self, client: FlaskClient) -> None:
        pass

    def test_missing_get_route_code(self, client: FlaskClient) -> None:
        r = client.get("/missing-route")
        self.assertIn(r.status_code, (404, 405))

    def test_missing_post_route_code(self, client: FlaskClient) -> None:
        r = client.post("/missing-route")
        self.assertIn(r.status_code, (404, 405))

    def test_missing_put_route_code(self, client: FlaskClient) -> None:
        r = client.put("/missing-route")
        self.assertIn(r.status_code, (404, 405))

    def test_missing_delete_route_code(self, client: FlaskClient) -> None:
        r = client.delete("/missing-route")
        self.assertIn(r.status_code, (404, 405))

    def test_user_get_route_code(self, client: FlaskClient) -> None:
        r = client.get("/user")
        self.assertNotIn(r.status_code, (404, 405))

    def test_user_post_route_code(self, client: FlaskClient) -> None:
        r = client.post("/user")
        self.assertNotIn(r.status_code, (404, 405))

    def test_user_put_route_code(self, client: FlaskClient) -> None:
        r = client.put("/user")
        self.assertNotIn(r.status_code, (404, 405))

    def test_user_delete_route_code(self, client: FlaskClient) -> None:
        r = client.delete("/user")
        self.assertNotIn(r.status_code, (404, 405))

    def test_exercise_get_route_code(self, client: FlaskClient) -> None:
        r = client.get("/exercise")
        self.assertNotIn(r.status_code, (404, 405))

    def test_exercise_post_route_code(self, client: FlaskClient) -> None:
        r = client.post("/exercise")
        self.assertNotIn(r.status_code, (404, 405))

    def test_exercise_put_route_code(self, client: FlaskClient) -> None:
        r = client.put("/exercise")
        self.assertNotIn(r.status_code, (404, 405))

    def test_exercise_delete_route_code(self, client: FlaskClient) -> None:
        r = client.delete("/exercise")
        self.assertNotIn(r.status_code, (404, 405))

    def test_solution_get_route_code(self, client: FlaskClient) -> None:
        r = client.get("/solution")
        self.assertNotIn(r.status_code, (404, 405))

    def test_solution_post_route_code(self, client: FlaskClient) -> None:
        r = client.post("/solution")
        self.assertNotIn(r.status_code, (404, 405))

    def test_solution_put_route_code(self, client: FlaskClient) -> None:
        r = client.put("/solution")
        self.assertNotIn(r.status_code, (404, 405))

    def test_solution_delete_route_code(self, client: FlaskClient) -> None:
        r = client.delete("/solution")
        self.assertNotIn(r.status_code, (404, 405))

    def test_login_get_route_code(self, client: FlaskClient) -> None:
        r = client.get("/login")
        self.assertIn(r.status_code, (404, 405))

    def test_login_post_route_code(self, client: FlaskClient) -> None:
        r = client.post("/login")
        self.assertNotIn(r.status_code, (404, 405))

    def test_login_put_route_code(self, client: FlaskClient) -> None:
        r = client.put("/login")
        self.assertIn(r.status_code, (404, 405))

    def test_login_delete_route_code(self, client: FlaskClient) -> None:
        r = client.delete("/login")
        self.assertIn(r.status_code, (404, 405))

    def test_logout_get_route_code(self, client: FlaskClient) -> None:
        r = client.get("/logout")
        self.assertIn(r.status_code, (404, 405))

    def test_logout_post_route_code(self, client: FlaskClient) -> None:
        r = client.post("/logout")
        self.assertIn(r.status_code, (404, 405))

    def test_logout_put_route_code(self, client: FlaskClient) -> None:
        r = client.put("/logout")
        self.assertIn(r.status_code, (404, 405))

    def test_logout_delete_route_code(self, client: FlaskClient) -> None:
        r = client.delete("/logout")
        self.assertNotIn(r.status_code, (404, 405))


if __name__ == "__main__":
    flask_unittest.main()
