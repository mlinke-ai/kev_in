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

from backend import create_app


class BaseTest(ClientTestCase):
    app = create_app("testing.cfg")
    base_header = {"Content-Type": "application/json"}

    def setUp(self, client: FlaskClient) -> None:
        raise NotImplementedError

    def tearDown(self, client: FlaskClient) -> None:
        raise NotImplementedError


@unittest.skip("Work in progress")
class SolutionTest(BaseTest):
    toDelete = []

    @classmethod
    def setUpClass(cls) -> None:
        # log in into sadmin
        r = requests.request(
            "POST",
            "/login",
            json={"user_mail": "sadmin@example.com", "user_pass": "sadmin"},
            headers={"Content-Type": "application/json"},
        )
        cls.adminCookie = r.headers["Set-Cookie"]

        # log in into tuser
        r = requests.request(
            "POST",
            "/login",
            json={"user_mail": "tuser@example.com", "user_pass": "tuser"},
            headers={"Content-Type": "application/json"},
        )
        cls.userCookie = r.headers["Set-Cookie"]

    @classmethod
    def tearDownClass(cls) -> None:
        for id in cls.toDelete:
            requests.request(
                "DELETE",
                "/solution",
                json={"solution_id": id},
                headers={"Cookie": f"{cls.adminCookie}"},
            )

    # --- GET ---

    def test_get_existing_by_id(self, client: FlaskClient) -> None:
        arg = 1
        r = client.get(
            f"/solution?solution_id={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"][0]["solution_id"], arg)

    def test_get_existing_by_user(self, client: FlaskClient) -> None:
        arg = 1
        r = client.get(
            f"/solution?solution_user={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"][0]["solution_user"], arg)

    def test_get_existing_by_exercise(self, client: FlaskClient) -> None:
        arg = 1
        r = client.get(
            f"/solution?solution_exercise={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"][0]["solution_exercise"], arg)

    def test_get_existing_by_date(self, client: FlaskClient) -> None:
        arg = 1234567890
        r = client.get(
            f"/solution?solution_date={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"][0]["solution_date"], "Sat, 14 Feb 2009 00:31:30 GMT")

    def test_get_existing_by_duration(self, client: FlaskClient) -> None:
        arg = 0
        r = client.get(
            f"/solution?solution_duration={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"][0]["solution_duration"], arg)

    def test_get_existing_by_correct(self, client: FlaskClient) -> None:
        arg = True
        r = client.get(
            f"/solution?solution_correct={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"][0]["solution_correct"], arg)

    def test_get_existing_by_pending(self, client: FlaskClient) -> None:
        arg = True
        r = client.get(
            f"/solution?solution_pending={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"][0]["solution_pending"], arg)

    def test_get_existing_by_content(self, client: FlaskClient) -> None:
        arg = {"solution": "some JSON"}
        r = client.get(
            f"/solution?solution_content={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"][0]["solution_content"], arg)

    def test_get_non_existing_by_id(self, client: FlaskClient) -> None:
        arg = -1
        r = client.get(
            f"/solution?solution_id={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"], [])

    def test_get_non_existing_by_user_id(self, client: FlaskClient) -> None:
        arg = -1
        r = client.get(
            f"/solution?solution_user={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"], [])

    def test_get_non_existing_by_exercise_id(self, client: FlaskClient) -> None:
        arg = -1
        r = client.get(
            f"/solution?solution_exercise={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"], [])

    def test_get_non_existing_by_date(self, client: FlaskClient) -> None:
        arg = 237459832  # hopefully this date does not exist in the database
        r = client.get(
            f"/solution?solution_date={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"], [])

    def test_get_non_existing_by_duration(self, client: FlaskClient) -> None:
        arg = -1
        r = client.get(
            f"/solution?solution_duration={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"], [])

    def test_get_non_existing_by_correct(self, client: FlaskClient) -> None:
        pass  # only True and False possible here

    def test_get_non_existing_by_pending(self, client: FlaskClient) -> None:
        pass  # only True and False possible here

    def test_get_non_existing_by_content(self, client: FlaskClient) -> None:
        arg = {"cont3nt": 1, "trash_data": "This dict should not be possible"}
        r = client.get(
            f"/solution?solution_content={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"], arg)

    def test_get_restrict_page_size(self, client: FlaskClient) -> None:
        arg = 2
        r = client.get(
            f"/solution?solution_limit={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(len(r.json["data"]), arg)

    def test_get_large_page_number(self, client: FlaskClient) -> None:
        r = client.get(
            f"/exercise?solution_page=4000",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["meta"]["prev_page"], None)
        self.assertEqual(r.json["meta"]["prev_url"], None)

    def test_get_user_not_own_data(self, client: FlaskClient) -> None:
        r = client.get(
            f"/solution?solution_user=1",
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        self.assertEqual(r.status_code, 403)
        self.assertTrue(r.is_json)

    def test_get_user_own_data(self, client: FlaskClient) -> None:
        r = client.get(
            f"/solution?solution_user=2",
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["data"][0]["solution_user"], 2)

    def test_get_no_login(self, client: FlaskClient) -> None:
        r = client.get(
            f"/solution",
            headers={"Cookie": f"key=value"},
        )
        self.assertEqual(r.status_code, 401)
        self.assertTrue(r.is_json)

    # --- POST ---

    def test_create_as_user(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 1,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "Successfully submitted solution")

    def test_create_as_admin(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "Successfully submitted solution")

    def test_create_without_token(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"key=value"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 401)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "Login required")

    def test_create_without_exercise_id(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        self.assertIn("solution_exercise", r.json["message"])

    def test_create_with_date_in_past(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 0,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "Successfully submitted solution")

    def test_create_with_negative_duration(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": -524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "Successfully submitted solution")

    def test_create_with_empty_content(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={"solution_exercise": 3, "solution_date": 123456789, "solution_duration": 524},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)
        self.assertIn("solution_content", r.json["message"])

    def test_create_with_malformed_content(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={"solution_exercise": 3, "solution_date": 123456789, "solution_duration": 524, "solution_content": {}},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["message"], "Successfully submitted solution")
        self.assertEqual(r.json["solution_correct"], False)

    def test_create_with_non_existing_exercise(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": -1,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)

    def test_create_right_parsons_puzzle(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["solution_correct"], True)

    def test_create_wrong_parsons_puzzle(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "is", "this", "exercise", "first", "the"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["solution_correct"], False)

    def test_create_right_coding_exercise(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 7,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {
                    "code": """
def multiply(x, y):
    return x*y
"""
                },
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["solution_correct"], True)

    def test_create_wrong_coding_exercise(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 7,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {
                    "code": """
def multiply(x, y):
    return x+y
"""
                },
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["solution_correct"], False)

    def test_create_right_gap_text_exercise(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 1,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"gap_entries": ["1", "2", "3"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["solution_correct"], True)

    def test_create_wrong_gap_text_exercise(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 1,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"gap_entries": ["1", "no clue", "3"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertTrue(r.is_json)
        self.assertEqual(r.json["solution_correct"], False)

    # --- PUT ---

    def test_change_existing(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={
                "solution_id": 3,
                "solution_exercise": 5,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_correct": False,
                "solution_pending": True,
                "solution_content": {"list": ["Hello", "World", "is", "this", "exercise", "first", "the"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)

    def test_change_non_existing(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={"solution_id": -1, "solution_date": 123456789},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 404)
        self.assertTrue(r.is_json)

    def test_change_as_user(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={"solution_id": 1, "solution_date": 3425234},
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        self.assertEqual(r.status_code, 403)
        self.assertTrue(r.is_json)

    def test_change_as_admin(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={"solution_id": 1, "solution_date": 3425234},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)

    def test_change_without_token(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={"solution_id": 1, "solution_date": 3425234},
            headers={"Cookie": f"key=value"},
        )
        self.assertEqual(r.status_code, 401)
        self.assertTrue(r.is_json)

    def test_change_to_empty_user(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={"solution_id": 1, "solution_user": -1},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)

    def test_change_to_empty_exercise(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={"solution_id": 1, "solution_user": -1},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(r.is_json)

    def test_change_to_date_in_past(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={"solution_id": 1, "solution_date": 0},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)

    def test_change_to_negative_duration(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={"solution_id": 1, "solution_duration": -534},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)

    def test_change_to_malformed_content(self, client: FlaskClient) -> None:
        r = client.put(
            "/solution",
            json={"solution_id": 1, "solution_content": {}},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)

    # --- DELETE ---

    def test_delete_as_admin(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            self.assertTrue(r.is_json)
            id = r.json["solution_id"]
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            self.fail("Failed to create exercise")

        r = client.delete(
            "/solution",
            json={"solution_id": id},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)

    def test_delete_non_existing(self, client: FlaskClient) -> None:
        r = client.delete(
            "/solution",
            json={"solution_id": -1},
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 404)
        self.assertTrue(r.is_json)

    def test_delete_own_as_user(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        try:
            self.assertTrue(r.is_json)
            id = r.json["solution_id"]
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            self.fail("Failed to create exercise")

        r = client.delete(
            "/solution",
            json={"solution_id": id},
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.is_json)

    def test_delete_other_as_user(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        try:
            self.assertTrue(r.is_json)
            id = r.json["solution_id"]
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            self.fail("Failed to create exercise")

        r = client.delete(
            "/solution",
            json={"solution_id": id},
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        self.assertEqual(r.status_code, 403)
        self.assertTrue(r.is_json)

    def test_delete_without_token(self, client: FlaskClient) -> None:
        r = client.post(
            "/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]},
            },
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        try:
            self.assertTrue(r.is_json)
            id = r.json["solution_id"]
            SolutionTest.toDelete.append(r.json["solution_id"])
        except KeyError:
            self.fail("Failed to create exercise")

        r = client.delete("/solution", json={"solution_id": id}, headers={"Cookie": f"key=value"})
        self.assertEqual(r.status_code, 401)
        self.assertTrue(r.is_json)


if __name__ == "__main__":
    flask_unittest.main()
