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


class UserTest(flask_unittest.ClientTestCase):
    app = create_app()

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self, client: FlaskClient) -> None:
        pass

    def tearDown(self, client: FlaskClient) -> None:
        pass

    # --- GET ---

    def test_get_existing_by_id(self, client: FlaskClient) -> None:
        r = client.get("/user", json={"user_id": 1})
        self.assertEqual(r.status_code, 200)

    def test_get_existing_by_name(self, client: FlaskClient) -> None:
        pass

    def test_get_existing_by_mail(self, client: FlaskClient) -> None:
        pass

    def test_get_existing_by_role(self, client: FlaskClient) -> None:
        pass

    def test_get_non_existing_by_id(self, client: FlaskClient) -> None:
        pass

    def test_get_non_existing_by_name(self, client: FlaskClient) -> None:
        pass

    def test_get_non_existing_by_mail(self, client: FlaskClient) -> None:
        pass

    def test_get_non_existing_by_role(self, client: FlaskClient) -> None:
        pass

    def test_get_restrict_page_size(self, client: FlaskClient) -> None:
        pass

    # --- POST ---

    def test_post_user(self, client: FlaskClient) -> None:
        pass

    def test_post_admin(self, client: FlaskClient) -> None:
        pass

    def test_post_user_without_token(self, client: FlaskClient) -> None:
        pass

    def test_post_duplicate_user(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_empty_name(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_empty_mail(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_empty_password(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_long_name(self, client: FlaskClient) -> None:
        pass

    def test_post_user_with_strange_name(self, client: FlaskClient) -> None:
        pass

    # --- PUT ---

    def test_put_mail_to_existing(self, client: FlaskClient) -> None:
        pass

    def test_put_name_to_empty(self, client: FlaskClient) -> None:
        pass

    def test_put_mail_to_empty(self, client: FlaskClient) -> None:
        pass

    def test_put_password_to_empty(self, client: FlaskClient) -> None:
        pass

    def test_put_admin_elevation_as_user(self, client: FlaskClient) -> None:
        pass

    def test_put_sadmin_elevation_as_user(self, client: FlaskClient) -> None:
        pass

    def test_put_admin_elevation_as_admin(self, client: FlaskClient) -> None:
        pass

    def test_put_sadmin_elevation_as_admin(self, client: FlaskClient) -> None:
        pass

    def test_put_demotion_as_user(self, client: FlaskClient) -> None:
        pass

    def test_put_demotion_as_admin(self, client: FlaskClient) -> None:
        pass

    # --- DELETE ---

    def test_delete_existing(self, client: FlaskClient) -> None:
        pass

    def test_delete_non_existing(self, client: FlaskClient) -> None:
        pass

    def test_delete_self_as_admin(self, client: FlaskClient) -> None:
        pass

    def test_delete_self_as_user(self, client: FlaskClient) -> None:
        pass

    def test_delete_other_as_admin(self, client: FlaskClient) -> None:
        pass

    def test_delete_other_as_user(self, client: FlaskClient) -> None:
        pass


if __name__ == "__main__":
    flask_unittest.main()
