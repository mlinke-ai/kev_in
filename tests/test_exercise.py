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
    """
    This test class tests the HTTP-request types of the Exercise endpoint. Therefor the class creates
    a test exercise and a test user and logs into an admin account and a user account (see setUpClass method).
    The documentation of the API can be found [here](https://mlinke-ai.github.io/kev_in/api/exercise/).
    Note: all tests Use the IP 127.0.0.1 and Port 5000, so the server which provides the endpoint should be hosted there.
    """

    exercise_title = "Test Parsons Puzzle"
    exercise_description = "This is a test Parsosns Puzzle"
    exercise_type = 3
    exercise_content = {"list": ["Hello", "this", "World", "is", "the", "first", "exercise"]}
    exercise_solution = {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
    exercise_language = 1
    exercise_id_list = []

    @classmethod
    def setUpClass(cls) -> None:
        # log into sadmin
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "sadmin@example.com", "user_pass": "sadmin"},
            headers={"Content-Type": "application/json"},
        )
        cls.adminCookie = r.headers["Set-Cookie"]

        # log into tuser
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_mail": "tuser@example.com", "user_pass": "tuser"},
            headers={"Content-Type": "application/json"},
        )
        cls.userCookie = r.headers["Set-Cookie"]

        # create an exercise which we can later edit or access
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": ExerciseTest.exercise_title,
                "exercise_description": ExerciseTest.exercise_description,
                "exercise_type": ExerciseTest.exercise_type,
                "exercise_content": ExerciseTest.exercise_content,
                "exercise_solution": ExerciseTest.exercise_solution,
                "exercise_language": ExerciseTest.exercise_language,
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )
        cls.exercise_id = r.json()["exercise_id"]

        # generate additional dummy exercises
        for i in range(20):
            r = requests.request(
                "POST",
                "http://127.0.0.1:5000/exercise",
                json={
                    "exercise_title": f"UnitTestDummyEx{i}",
                    "exercise_description": "Dummy for exercise UnitTests",
                    "exercise_type": 1,
                    "exercise_content": {},
                    "exercise_solution": {},
                    "exercise_language": 2,
                },
                headers={
                    "Content-Type": "application/json",
                    "Cookie": f"{ExerciseTest.adminCookie}",
                },
            )
            ExerciseTest.exercise_id_list.append(r.json()["exercise_id"])

    @classmethod
    def tearDownClass(cls) -> None:
        # delete the created exercise
        requests.request(
            "DELETE",
            "http://127.0.0.1:5000/exercise",
            json={"exercise_id": ExerciseTest.exercise_id},
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )
        cls.exercise_id = None

        # delete dummy exercises
        for i in range(20):
            r = requests.request(
                "DELETE",
                "http://127.0.0.1:5000/exercise",
                json={
                    "exercise_id": ExerciseTest.exercise_id_list[i],
                },
                headers={
                    "Content-Type": "application/json",
                    "Cookie": f"{ExerciseTest.adminCookie}",
                },
            )

    # ------------------------------HTTP-GET-----------------------------

    def test_get_existing_by_id(self) -> None:
        """
        Query the System for an existing exercise with a HTTP-GET request by id with admin account.
        The system should return HTTP-status 200 and the attributes of the exercise in JSON format.
        """

        arg = ExerciseTest.exercise_id
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_id={arg}&exercise_details=true",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["exercise_id"], arg)

    def test_get_existing_by_title(self) -> None:
        arg = ExerciseTest.exercise_title
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_title={arg}&exercise_details=true",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["exercise_title"], arg)

    def test_get_existing_by_type(self) -> None:
        arg = ExerciseTest.exercise_type
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_type={arg}&exercise_details=true",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["exercise_type_value"], arg)

    def test_get_existing_by_description(self) -> None:
        arg = ExerciseTest.exercise_description
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_description={arg}&exercise_details=true",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["exercise_description"], arg)

    def test_get_existing_by_content(self) -> None:
        arg = ExerciseTest.exercise_content
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_content={arg}&exercise_details=true",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["exercise_content"], arg)

    def test_get_existing_by_solution(self) -> None:
        arg = ExerciseTest.exercise_solution
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_solution={arg}&exercise_details=true",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["exercise_solution"], arg)

    def test_get_existing_by_language(self) -> None:
        arg = ExerciseTest.exercise_language
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_language={arg}&exercise_details=true",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][0]["exercise_language_value"], arg)

    def test_get_paging(self) -> None:
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_page=2",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(r.json()["meta"]["prev_page"], None)
        self.assertNotEqual(r.json()["meta"]["prev_url"], None)

    def test_get_limit(self) -> None:
        arg = 4
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_limit={arg}",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()["data"]), arg)

    def test_get_details_false(self) -> None:
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_details=false",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertNotIn("exercise_description", r.json()["data"][0])
        self.assertNotIn("exercise_content", r.json()["data"][0])
        self.assertNotIn("exercise_solution", r.json()["data"][0])

    def test_get_details_true(self) -> None:
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_details=true",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("exercise_id", r.json()["data"][0])
        self.assertIn("exercise_title", r.json()["data"][0])
        self.assertIn("exercise_description", r.json()["data"][0])
        self.assertIn("exercise_type_name", r.json()["data"][0])
        self.assertIn("exercise_type_value", r.json()["data"][0])
        self.assertIn("exercise_content", r.json()["data"][0])
        self.assertIn("exercise_solution", r.json()["data"][0])
        self.assertIn("exercise_language_name", r.json()["data"][0])
        self.assertIn("exercise_language_value", r.json()["data"][0])

    def test_get_non_existing(self) -> None:
        """
        Query the System for a non existing exercise with a HTTP-GET request by id with admin account.
        The system should return HTTP-status 200 and an empty JSON string.
        """
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_id=-2",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        # HTTP status 200 and empty JSON
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.json()["data"], [])

    def test_get_existing_user(self) -> None:
        """
        Query the System for an existing exercise with HTTP-GET by id as logged in user.
        The system should return HTTP-status 200 and the attributes of the exercise in JSON format.
        """

        id = str(ExerciseTest.exercise_id)
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_id={id}&exercise_details=true",
            headers={"Cookie": f"{ExerciseTest.userCookie}"},
        )
        self.assertEqual(r.status_code, 200)

    def test_get_existing_no_login(self) -> None:
        """
        Query the System for an existing exercise with HTTP-GET by id as logged out client (no token in cookie).
        The system should return HTTP-status 401 and an error message.
        """

        id = ExerciseTest.exercise_id
        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_id={id}",
            headers={"Cookie": f"key=value"},
        )
        self.assertEqual(r.status_code, 401)
        self.assertDictEqual(r.json(), {"message": "Login required"})

    # ------------------------------HTTP-POST-----------------------------

    def test_post_success(self) -> None:
        """
        Create an exercise in the system with HTTP-POST method with a logged in admin account.
        The system should return HTTP-status 201, the created exercise in JSON and a
        success message.
        """

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "My Exercise",
                "exercise_description": "This is a good Test example!",
                "exercise_type": 1,
                "exercise_content": {},
                "exercise_solution": {},
                "exercise_language": 1,
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )
        self.assertEqual(r.status_code, 201)

        try:
            exercise = r.json()
        except KeyError:
            self.fail("An exercise should be returned")

        # returned exercise should have these attributes
        self.assertIn("exercise_id", exercise)
        self.assertIn("exercise_title", exercise)
        self.assertEqual("The exercise was created successfully", exercise["message"])

        id = exercise["exercise_id"]

        requests.request(
            "DELETE",
            "http://127.0.0.1:5000/exercise",
            json={"exercise_id": id},
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )

    def test_post_no_access(self) -> None:
        """
        Create an exercise in the system with HTTP-POST method without logging in or with a user account.
        The system should return HTTP-status 401 or 403
        """

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "My Exercise",
                "exercise_description": "This is a good Test example!",
                "exercise_type": 1,
                "exercise_content": {},
                "exercise_solution": {},
                "exercise_language": 1,
            },
            headers={"Content-Type": "application/json", "Cookie": "key=value;"},
        )
        self.assertDictEqual(r.json(), {"message": "Login required"})
        self.assertEqual(r.status_code, 401)

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "My Exercise",
                "exercise_description": "This is a good Test example!",
                "exercise_type": 1,
                "exercise_content": {},
                "exercise_solution": {},
                "exercise_language": 1,
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.userCookie}",
            },
        )
        self.assertDictEqual(r.json(), {"message": "No Access"})
        self.assertEqual(r.status_code, 403)

    def test_post_existing(self) -> None:
        """
        Attempting to create/overwrite an already existing exercise with the HTTP-POST method.
        Overwriting exercises should not be possible even with admin privileges
        This test should return HTTP-status 400 and an error message stating the issue.
        """

        title = f"{ExerciseTest.exercise_title}"

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": title,
                "exercise_description": "This is a good Test example!",
                "exercise_type": 1,
                "exercise_content": {},
                "exercise_solution": {},
                "exercise_language": 1,
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )

        try:
            exercise = r.json()
        except KeyError:
            self.fail("An exercise should be returned")

        self.assertEqual(r.status_code, 409)

        # Response should include a fail message
        self.assertEqual("An exercise with this title already exists", exercise["message"])

    def test_post_without_req_arg(self) -> None:
        """
        Create a new exercise with HTTP-POST method but without one required argument (exercise_content).
        The system should return HTTP-status 400 and an error message containing the missing argument.
        """

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "My Exercise",
                "exercise_description": "This is a good Test example!",
                "exercise_type": 1,
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )

        self.assertEqual(r.status_code, 400)
        try:
            errors = r.json()["message"]
        except KeyError:
            self.fail("An error message should be returned")

        self.assertIn("exercise_content", errors)

    # ------------------------------HTTP-PUT-----------------------------

    def test_put_existing(self) -> None:
        """
        Change all attributes of an existing exercise with HTTP-PUT method with admin account.
        The system should return HTTP-status 200 and a success message.
        """

        id = str(ExerciseTest.exercise_id)
        # test changing all attributes
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "CoolExercise",
                "exercise_id": id,
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": {},
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )
        self.assertDictEqual(
            r.json(),
            {"message": f"Successfully changed exercise with exercise_id {id}"},
        )
        self.assertEqual(r.status_code, 200)

    def test_put_existing_user(self) -> None:
        """
        Change all attributes of an existing exercise with HTTP-PUT method with user account.
        The system should return HTTP-status 403 and an error message.
        """

        id = str(ExerciseTest.exercise_id)
        # test changing all attributes
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "CoolExercise",
                "exercise_id": id,
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": {},
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.userCookie}",
            },
        )
        self.assertDictEqual(r.json(), {"message": "No Access"})
        self.assertEqual(r.status_code, 403)

    def test_put_existing_no_login(self) -> None:
        """
        Change all attributes of an existing exercise with HTTP-PUT method with a logged in user account.
        The system should return HTTP-status 401 and an error message.
        """

        id = str(ExerciseTest.exercise_id)
        # test changing all attributes
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "CoolExercise",
                "exercise_id": id,
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": {},
            },
            headers={"Content-Type": "application/json", "Cookie": "key=value;"},
        )
        self.assertDictEqual(r.json(), {"message": "Login required"})
        self.assertEqual(r.status_code, 401)

    def test_put_without_req_arg(self) -> None:
        """
        Change all attributes of an existing exercise with HTTP-PUT method but without the required argument (exercise_id).
        The system should return HTTP-status 400 and an error message containing the missing argument.
        """

        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "CoolExercise",
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": {},
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )

        # server should return HTTP status 400
        self.assertEqual(r.status_code, 400)
        try:
            errors = r.json()["message"]
        except KeyError:
            self.fail("An error message should be returned")

        self.assertIn("exercise_id", errors)

    def test_put_non_existing(self) -> None:
        """
        Change all attributes of a non existing exercise with HTTP-PUT method.
        The system should return HTTP-status 404 and an error message.
        """

        id = -2  # exercise_id of a clearly not existing exercise
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_id": id,
                "exercise_title": "CoolExercise",
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": {},
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )

        self.assertIn("message", r.json())
        self.assertEqual(r.json()["message"], f"Exercise with exercise_id {id} does not exist")
        self.assertEqual(r.status_code, 404)

    # ------------------------------HTTP-DELETE-----------------------------

    def test_delete_existing(self) -> None:
        """
        Attempting deleting an existing task in the Database using its ID with the HTTP-DELETE method.
        First using user access then admin privileges
        This system should return HTTP-status 403 then 200 and its success message should include the correct id
        NOTE: It is necessary to first successfully create a task to delete. Deleting the main task interferes with other tests.
        """

        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "To Be Deleted",
                "exercise_description": "This is a good Test example!",
                "exercise_type": 1,
                "exercise_content": {},
                "exercise_solution": {},
                "exercise_language": 1,
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )
        self.assertEqual(r.status_code, 201)

        try:
            exercise = r.json()
        except KeyError:
            self.fail("An exercise should be returned")

        id = exercise["exercise_id"]

        # Fail Case #1:

        r = requests.request(
            "DELETE",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_id": id,
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.userCookie}",
            },
        )

        self.assertEqual(r.status_code, 403)
        self.assertDictEqual(r.json(), {"message": "No Access"})

        # Fail Case #2:

        r = requests.request(
            "DELETE",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_id": id,
            },
            headers={"Content-Type": "application/json", "Cookie": "key=value;"},
        )

        self.assertEqual(r.status_code, 401)
        self.assertDictEqual(r.json(), {"message": "Login required"})

        # Success Case:

        r = requests.request(
            "DELETE",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_id": id,
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )

        self.assertEqual(r.status_code, 200)
        self.assertIn("message", r.json())
        self.assertEqual(r.json()["message"], f"Successfully deleted exercise with exercise_id {id}")

    def test_delete_non_existing(self) -> None:
        """
        Delete a non-existing task in the database using id = -2 with the HTTP-DELETE method with admin privileges
        This system should return HTTP-status 404 stating exercise id does not exist
        """

        id = -2  # exercise_id of a clearly not existing exercise

        r = requests.request(
            "DELETE",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_id": id,
            },
            headers={
                "Content-Type": "application/json",
                "Cookie": f"{ExerciseTest.adminCookie}",
            },
        )

        self.assertEqual(r.status_code, 404)
        self.assertIn("message", r.json())
        self.assertEqual(r.json()["message"], f"Exercise with exercise_id {id} does not exist")


if __name__ == "__main__":
    unittest.main()
