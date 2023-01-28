#!/usr/bin/python3
# -*- coding: utf-8 -*-

import enum
import string
import secrets

#generate a random 64 letter password
alphabet = string.ascii_letters + string.digits + '!@#$%^&*()_'
tmp = ''.join(secrets.choice(alphabet) for i in range(64))

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

JWT_SECRET = tmp

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
