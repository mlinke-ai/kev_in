#!/usr/bin/env python3
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

import requests

# # sign up
# r = requests.request("POST", "http://127.0.0.1:5000/user", json={"user_name": "test_user", "user_pass": "12341234",
#                      "user_mail": "test@example.com", "user_role": 3}, headers={"Content-Type": "application/json"})
# print(r.status_code)

# sign in as admin
r = requests.request(
    "POST",
    "http://127.0.0.1:5000/login",
    json={"user_mail": "sadmin@example.com", "user_pass": "sadmin"},
    headers={"Content-Type": "application/json"},
)
token = r.cookies.get("token")
print("sadmin login: ", r.status_code)

# delete an ParsonsPuzzleExercise
r = requests.request(
    "DELETE",
    "http://127.0.0.1:5000/exercise",
    json={
        "exercise_id": 1,
    },
    headers={"Content-Type": "application/json", "Cookie": "token=" + token},
)
print("delete ppe: ", r.status_code)

# # create an ParsonsPuzzleExercise
# r = requests.request(
#   "POST",
#   "http://127.0.0.1:5000/exercise",
#   json={
#     "exercise_title": "hallo",
#     "exercise_description": "Place the items in the correct order!",
#     "exercise_type": 3,
#     "exercise_content": "[{id: 1, name: import math}, {id: 2, name: print (math.pi)}]",
#     "exercise_solution": "[{id: 1, name: import math}, {id: 2, name: print (math.pi)}]",
#     "exercise_language": 1
#   },
#   headers={
#     "Content-Type": "application/json",
#     "Cookie": "token="+token
#   },
# )
# print("ppe creation: ", r.status_code)

# retrieve an ParsonsPuzzleExercise
r = requests.request(
    "GET",
    "http://127.0.0.1:5000/exercise?exercise_type=3&exercise_details=true",
    headers={"Content-Type": "application/json", "Cookie": "token=" + token},
)

print("retrieve ppe: ", r.status_code, r.content)
