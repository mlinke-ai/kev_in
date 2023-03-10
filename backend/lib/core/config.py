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

import enum

SADMIN_NAME = "sadmin"
SADMIN_PASS = "sadmin"
SADMIN_MAIL = "sadmin@example.com"

TUSER_NAME = "tuser"
TUSER_PASS = "tuser"
TUSER_MAIL = "tuser@example.com"

# dialect://username:password@host:port/database
DATABASE_URI = ""
TESTING_DATABASE_URI = "sqlite:///testing.db"

USER_TABLE = "users"
EXERCISE_TABLE = "exercises"
SOLUTION_TABLE = "solutions"

MAX_ITEMS_RETURNED = 20


class UserRole(enum.IntEnum):
    SAdmin = 1
    Admin = 2
    User = 3


class ExerciseType(enum.IntEnum):
    GapTextExercise = 1
    SyntaxExercise = 2
    ParsonsPuzzleExercise = 3
    FindTheBugExercise = 4
    DocumentationExercise = 5
    OutputExercise = 6
    ProgrammingExercise = 7


class ExerciseLanguage(enum.IntEnum):
    Python = 1
    Java = 2
