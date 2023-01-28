#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

#you should generate a very safe password for that
JWT_SECRET = "WL2pmWo1[;|Y<9\nyva@sG0vB0W=BFhq/Pix^gVeR^-}!com_t+4G7gh&>@)e1N"

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
