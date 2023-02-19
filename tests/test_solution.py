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

class SolutionTest(unittest.TestCase):

    toDelete = []

    @classmethod
    def setUpClass(cls) -> None:
        #log in into sadmin
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "sadmin@example.com", "user_pass": "sadmin"},
            headers={"Content-Type": "application/json"},
        )
        cls.adminCookie = r.headers["Set-Cookie"]

        #log in into tuser
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "tuser@example.com", "user_pass": "tuser"},
            headers={"Content-Type": "application/json"},
        )
        cls.userCookie = r.headers["Set-Cookie"]

    @classmethod
    def tearDownClass(cls) -> None:
        
        for id in cls.toDelete:
            requests.request(
                "DELETE",
                "http://127.0.0.1:5000/solution",
                json={"solution_id": id},
                headers={"Cookie": f"{cls.adminCookie}"},
            )

    # --- GET ---

    def test_get_existing_by_id(self) -> None:
        
        arg = 1
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_id={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["solution_id"], arg)

    def test_get_existing_by_user(self) -> None:
        
        arg = 1
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_user={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["solution_user"], arg)

    def test_get_existing_by_exercise(self) -> None:

        arg = 1
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_exercise={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["solution_exercise"], arg)

    def test_get_existing_by_date(self) -> None:
        
        arg = 1234567890
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_date={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["solution_date"], "Sat, 14 Feb 2009 00:31:30 GMT")

    def test_get_existing_by_duration(self) -> None:
        
        arg = 0
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_duration={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["solution_duration"], arg)

    def test_get_existing_by_correct(self) -> None:
        
        arg = True
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_correct={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["solution_correct"], arg)

    def test_get_existing_by_pending(self) -> None:
        
        arg = True
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_pending={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["solution_pending"], arg)

    def test_get_existing_by_content(self) -> None:
        
        arg = {"solution": "some JSON"}
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_content={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["solution_content"], arg)

    def test_get_non_existing_by_id(self) -> None:
        
        arg = -1
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_id={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"], [])

    def test_get_non_existing_by_user_id(self) -> None:
        
        arg = -1
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_user={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"], [])

    def test_get_non_existing_by_exercise_id(self) -> None:
        
        arg = -1
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_exercise={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"], [])

    def test_get_non_existing_by_date(self) -> None:
        
        arg = 0
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_date={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"], [])

    def test_get_non_existing_by_duration(self) -> None:
        
        arg = -1
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_duration={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"], [])

    def test_get_non_existing_by_correct(self) -> None:
        pass #only True and False possible here

    def test_get_non_existing_by_pending(self) -> None:
        pass #only True and False possible here

    def test_get_non_existing_by_content(self) -> None:
        
        arg = {"cont3nt": 1, "trash_data": "This dict should not be possible"}
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_content={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"], arg)

    def test_get_restrict_page_size(self) -> None:
        
        arg = 2
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_limit={arg}",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()["data"]), arg)

    def test_get_large_page_number(self) -> None:

        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?solution_page=4000",
            headers={"Cookie": f"{SolutionTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["meta"]["prev_page"], None)
        self.assertEqual(r.json()["meta"]["prev_url"], None)

    def test_get_user_not_own_data(self) -> None:
        
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_user=1",
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        self.assertEqual(r.status_code, 403)

    def test_get_user_own_data(self) -> None:
        
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution?solution_user=2",
            headers={"Cookie": f"{SolutionTest.userCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["solution_user"], 2)

    def test_get_no_login(self) -> None:
        
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/solution",
            headers={"Cookie": f"key=value"},
        )
        self.assertEqual(r.status_code, 401)

    # --- POST ---

    def test_create_as_user(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 1,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
            },
            headers={"Cookie": f"{SolutionTest.userCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "Successfully submitted solution")

    def test_create_as_admin(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "Successfully submitted solution")

    def test_create_without_token(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
            },
            headers={"Cookie": f"key=value"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.json()["message"], "Login required")

    def test_create_without_exercise_id(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 400)
        self.assertIn("solution_exercise", r.json()["message"])

    def test_create_with_date_in_past(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 0,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "Successfully submitted solution")

    def test_create_with_negative_duration(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": -524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "Successfully submitted solution")

    def test_create_with_empty_content(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 400)
        self.assertIn("solution_content", r.json()["message"])

    def test_create_with_malformed_content(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {}
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["message"], "Successfully submitted solution")
        self.assertEqual(r.json()["solution_correct"], False)

    def test_create_with_non_existing_exercise(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": -1,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 400)

    def test_create_right_parsons_puzzle(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["solution_correct"], True)

    def test_create_wrong_parsons_puzzle(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"list": ["Hello", "World", "is", "this", "exercise", "first", "the"]}
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["solution_correct"], False)

    def test_create_right_coding_exercise(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 7,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"code":
"""
def multiply(x, y):
    return x*y
"""          
                }
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["solution_correct"], True)

    def test_create_wrong_coding_exercise(self) -> None:
        
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/solution",
            json={
                "solution_exercise": 3,
                "solution_date": 123456789,
                "solution_duration": 524,
                "solution_content": {"code":
"""
def multiply(x, y):
    return x+y
"""          
                }
            },
            headers={"Cookie": f"{SolutionTest.adminCookie}"}
        )
        try:
            SolutionTest.toDelete.append(r.json()["solution_id"])
        except KeyError:
            pass
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["solution_correct"], False)

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

    def test_change_pending(self) -> None:
        pass

    def test_change_to_empty_content(self) -> None:
        pass

    def test_change_to_malformed_content(self) -> None:
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
