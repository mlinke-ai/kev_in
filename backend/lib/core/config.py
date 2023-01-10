#!/usr/bin/python3
# -*- coding: utf-8 -*-

import enum

SADMIN_NAME = "sadmin"
SADMIN_PASS = "sadmin"
SADMIN_MAIL = "sadmin@example.com"

USER_TABLE = "users"
EXERCISE_TABLE = "exercises"
SOLUTION_TABLE = "solutions"

JWT_SECRET = "9457645763984570345"

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
