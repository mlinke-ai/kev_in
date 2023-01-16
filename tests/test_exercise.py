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
    a test exercise and a test user and loggs into an admin account and a user account (see setUpClass method).
    The documentation of the API can be found [here](https://mlinke-ai.github.io/kev_in/api/exercise/).
    Note: all tests Use the IP 127.0.0.1 and Port 5000, so the server which provides the endpoint should be hosted there.
    """

    user_name = "G:ff#Test"
    user_pass = "hji'$4y33F?"

    @classmethod
    def setUpClass(cls) -> None:
        # log into sadmin
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_name": "sadmin", "user_pass": "sadmin"},
            headers={"Content-Type": "application/json"},
        )
        cls.adminCookie = r.headers["Set-Cookie"]

        # create an exercise which we can later edit or access
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "Dummy",
                "exercise_description": "Test",
                "exercise_type": 1,
                "exercise_content": "1+1=",
            },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
        )
        cls.exercise_id = r.json()["exercise_id"]
        cls.exercise_title = r.json()["exercise_title"]

        # create a test user which we can use later
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/user",
            json={
                "user_name": ExerciseTest.user_name,
                "user_pass": ExerciseTest.user_pass,
                "user_mail": "test@example.com",
                "user_role": 3,
            },
            headers={"Content-Type": "application/json"},
        )
        cls.user_id = r.json()["user_id"]

        # log into the created test user
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_name": ExerciseTest.user_name, "user_pass": ExerciseTest.user_pass},
            headers={"Content-Type": "application/json"},
        )
        cls.userCookie = r.headers["Set-Cookie"]

    @classmethod
    def tearDownClass(cls) -> None:
        # delete the created exercise
        requests.request(
            "DELETE",
            "http://127.0.0.1:5000/exercise",
            json={"exercise_id": ExerciseTest.exercise_id},
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
        )
        cls.exercise_id = None

        # log out of the user account
        cls.userCookie = None

        # delete the created user
        requests.request(
            "DELETE",
            "http://127.0.0.1:5000/user",
            json={"user_id": ExerciseTest.user_id},
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
        )
        cls.user_id = None

        # log out of admin account
        cls.adminCookie = None

    # ------------------------------HTTP-GET-----------------------------

    def test_get_existing(self) -> None:
        """
        Query the System for an existing exercise with a HTTP-GET request by id with admin account.
        The system should return HTTP-status 200 and the attributes of the exercise in JSON format.
        """

        id = str(ExerciseTest.exercise_id)

        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_id={id}",
            headers={"Cookie": f"{ExerciseTest.adminCookie}"},
        )
        # server should return HTTP status 200
        self.assertEqual(r.status_code, 200)
        try:
            exercise = r.json()[id]
        except KeyError:
            self.fail("An exercise should be returned")

        # returned exercise should have these attributes
        self.assertIn("exercise_content", exercise)
        self.assertIn("exercise_description", exercise)
        self.assertIn("exercise_id", exercise)
        self.assertIn("exercise_title", exercise)
        self.assertIn("exercise_type", exercise)

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
        # HTTP stauts 200 and empty JSON
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {})

    def test_get_existing_user(self) -> None:
        """
        Query the System for an existing exercise with HTTP-GET by id as logged in user.
        The system should return HTTP-status 200 and the attributes of the exercise in JSON format.
        """

        id = str(ExerciseTest.exercise_id)

        r = requests.request(
            "GET",
            f"http://127.0.0.1:5000/exercise?exercise_id={id}",
            headers={"Cookie": f"{ExerciseTest.userCookie}"},
        )
        # server should return HTTP status 200
        self.assertEqual(r.status_code, 200)
        try:
            exercise = r.json()[id]
        except KeyError:
            self.fail("An exercise should be returned")

        # returned exercise should have these attributes
        self.assertIn("exercise_content", exercise)
        self.assertIn("exercise_description", exercise)
        self.assertIn("exercise_id", exercise)
        self.assertIn("exercise_title", exercise)
        self.assertIn("exercise_type", exercise)

    def test_get_existing_no_login(self) -> None:
        """
        Query the System for an existing exercise with HTTP-GET by id as logged out client (no token in cookie).
        The system should return HTTP-status 401 and an error message.
        """

        id = str(ExerciseTest.exercise_id)

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
                "exercise_content": "1+1=",
            },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
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
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
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
                "exercise_content": "1+1=",
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
                "exercise_content": "1+1=",
            },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.userCookie}"},
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
                "exercise_content": "1+1=",
            },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
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
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
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
        # test changing all attribues
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "CoolExercise",
                "exercise_id": id,
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": "2+4=",
            },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
        )
        self.assertDictEqual(r.json(), {"message": f"Successfully chanaged exercise with exercise_id {id}"})
        self.assertEqual(r.status_code, 200)

    def test_put_existing_user(self) -> None:
        """
        Change all attributes of an existing exercise with HTTP-PUT method with user account.
        The system should return HTTP-status 403 and an error message.
        """

        id = str(ExerciseTest.exercise_id)
        # test changing all attribues
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "CoolExercise",
                "exercise_id": id,
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": "2+4=",
            },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.userCookie}"},
        )
        self.assertDictEqual(r.json(), {"message": "No Access"})
        self.assertEqual(r.status_code, 403)

    def test_put_existing_no_login(self) -> None:
        """
        Change all attributes of an existing exercise with HTTP-PUT method with a logged in user account.
        The system should return HTTP-status 401 and an error message.
        """

        id = str(ExerciseTest.exercise_id)
        # test changing all attribues
        r = requests.request(
            "PUT",
            "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "CoolExercise",
                "exercise_id": id,
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": "2+4=",
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
                "exercise_content": "2+4=",
            },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
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
                "exercise_content": "2+4=",
            },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
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
                "exercise_content": "1+1=",
            },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
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
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.userCookie}"},
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
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
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
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.adminCookie}"},
        )

        self.assertEqual(r.status_code, 404)
        self.assertIn("message", r.json())
        self.assertEqual(r.json()["message"], f"Exercise with exercise_id {id} does not exist")


if __name__ == "__main__":
    unittest.main()
