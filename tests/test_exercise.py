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
    This test class tests the HTTP req. types of the Exercise endpoint, with a logged in
    sadmin account and an existing exercise in the database. (see setUpClass method)
    The documentation of the API can be found [here](https://mlinke-ai.github.io/kev_in/api/exercise/).
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        #log into sadmin
        r = requests.request(
            "POST",
            "http://127.0.0.1:5000/login",
            json={"user_name": "sadmin", "user_pass": "sadmin"},
            headers={"Content-Type": "application/json"},
        )
        cls.cookie = r.headers["Set-Cookie"]

        #create an exercise which we can later edit or access
        r = requests.request(
            "POST", "http://127.0.0.1:5000/exercise",
            json={"exercise_title": "Dummy", "exercise_description" : "Test", "exercise_type": 1, "exercise_content":"1+1="},
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
        )
        cls.exercise_id = r.json()["exercise_id"]

    @classmethod
    def tearDownClass(cls) -> None: 
        #delete the created exercise
        requests.request(
            "DELETE", "http://127.0.0.1:5000/exercise",
            json={"exercise_id": ExerciseTest.exercise_id},
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
        )
        
        #log out of sadmin
        cls.cookie = ""

    def test_get_existing(self) -> None:
        """
        Query the System for an existing exercise with a HTTP-GET request by id.
        The system should return HTTP-status 200 and the attributes of the exercise in JSON format.
        """

        id = str(ExerciseTest.exercise_id)

        r = requests.request(
            "GET", f"http://127.0.0.1:5000/exercise?exercise_id={id}",
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
            )
        #server should return HTTP status 200
        self.assertEqual(r.status_code, 200)
        try:
            exercise = r.json()[id]
        except KeyError:
            self.fail("An exercise should be returned")
        
        #returned exercise should have these attributes
        self.assertIn("exercise_content", exercise)
        self.assertIn("exercise_description", exercise)
        self.assertIn("exercise_id", exercise)
        self.assertIn("exercise_title", exercise)
        self.assertIn("exercise_type", exercise)
        
    def test_get_non_existing(self) -> None:
        """
        Query the System for a non existing exercise with a HTTP-GET request by id.
        The system should return HTTP-status 200 and an empty JSON string.
        """
        r = requests.request(
            "GET", "http://127.0.0.1:5000/exercise?exercise_id=-2",
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
        )
        #HTTP stauts 200 and empty JSON
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {})

    def test_post_success(self) -> None:
        """
        Create an exercise in the system with HTTP-POST method.
        The system should return HTTP-status 201, the created exercise in JSON and a
        success message.
        """

        r = requests.request(
            "POST", "http://127.0.0.1:5000/exercise",
            json={"exercise_title": "MyExercise", "exercise_description" : "TestTestTest", "exercise_type": 1, "exercise_content":"1+1="},
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
        )
        self.assertEqual(r.status_code, 201)
        print(r.json()["message"])

        try:
            exercise = r.json()
        except KeyError:
            self.fail("An exercise should be returned")

        #returned exercise should have these attributes
        self.assertIn("exercise_id", exercise)
        self.assertIn("exercise_title", exercise)
        self.assertEqual("The exercise was created successfully", exercise["message"])

        id = exercise["exercise_id"]

        requests.request(
            "DELETE", "http://127.0.0.1:5000/exercise",
            json={"exercise_id": id },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
        )

    def test_put_existing(self) -> None:
        """
        Change all attributes of an existing exercise with HTTP-PUT method.
        The system should return HTTP-status 200 and a success message.
        """

        id = str(ExerciseTest.exercise_id)
        #test changing all attribues
        r = requests.request(
            "PUT", "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "CoolExercise",
                "exercise_id": id,
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": "2+4="
                },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
        )
        self.assertDictEqual(r.json(), {"message": f"Successfully chanaged exercise with exercise_id {id}"})
        self.assertEqual(r.status_code, 200)

    def test_put_without_req_arg(self) -> None:
        """
        Change all attributes of an existing exercise with HTTP-PUT method but without the required argument (exercise_id).
        The system should return HTTP-status 400 and an error message containing the missing argument.
        """

        r = requests.request(
            "PUT", "http://127.0.0.1:5000/exercise",
            json={
                "exercise_title": "CoolExercise",
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": "2+4="
                },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
        )

        #server should return HTTP status 400
        self.assertEqual(r.status_code, 400)
        try:
            errors = r.json()["message"]
        except KeyError:
            self.fail("An error message should be returned")

        self.assertIn("exercise_id", errors)
        self.assertEqual(errors["exercise_id"], "ID of the exercise is missing")

    def test_put_non_existing(self) -> None:
        """
        Change all attributes of a non existing exercise with HTTP-PUT method.
        The system should return HTTP-status 404 and an error message.
        """

        id = -2 #exercise_id of a clearly not existing exercise
        r = requests.request(
            "PUT", "http://127.0.0.1:5000/exercise",
            json={
                "exercise_id": id,
                "exercise_title": "CoolExercise",
                "exercise_description": "This is an Exercise",
                "exercise_type": 1,
                "exercise_content": "2+4="
                },
            headers={"Content-Type": "application/json", "Cookie": f"{ExerciseTest.cookie}"}
        )
        
        self.assertIn("message", r.json())
        self.assertEqual(r.json()["message"], f"Exercise with exercise_id {id} does not exist")
        self.assertEqual(r.status_code, 404)

if __name__ == "__main__":
    unittest.main()