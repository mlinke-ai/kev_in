---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2023-01-09
---

# Configuration

The `backend/lib/core/config.py` file defines some initial configurations and global names.

## SADMIN_NAME

The name with which the SAdmin account gets initialized. Defaults to `sadmin`.

## SADMIN_PASS

The password with which the SAdmin accounts gets initialized. Defaults to `sadmin`.

!!! warning "Security hazard"
    Change this password immediately after the first login.

## SADMIN_MAIL

The mail address with which the SAdmin account gets initialized. Defaults to `sadmin@example.com`.

## USER_TABLE

The table name of the user table. Defaults to `users`.

## EXERCISE_TABLE

The table name of the exercise table. Defaults to `exercises`.

## SOLUTION_TABLE

The table name of the solution table. Defaults to `solutions`.

## JWT_SECRET

The base seed which is used to encrypt and decrypt JSON Web Tokens. Defaults to `9457645763984570345`.

## MAX_ITEMS_RETURNED

The number of items which one request should return on maximum. This value is used to prevent overwhelming the server. Defaults to `20`.

## UserRole

An enumeration to standardize the user roles. The roles are as follows:

| ID | Role | Description |
|---|---|---|
| `1` | SAdmin | The super admin role. The super admin can do every thing a normal admin can do plus managing admin roles. There should be only one super admin. |
| `2` | Admin | A normal admin can create, change and delete exercises. The admin also has to evaluate solutions which can not be evaluated automatically. |
| `3` | User | A normal user of the system. The user can only get exercises and submit solutions. |

## ExerciseType

An enumeration to standardize exercise types. The types are as follows:

| ID | Type | Description |
|---|---|---|
| `1` | GapTextExercise | An exercise where the user has fill in blanks to complete a given program. |
| `2` | SyntaxExercise | An exercise where the user has to point out one ore more syntax errors in a given program. |
| `3` | ParsonsPuzzleExercise | An exercise where the user has to arrange given code blocks into the proper order. |
| `4` | FindTheBugExercise | An exercise where the user has point out one or more bugs in a given program. |
| `5` | DocumentationExercise | An exercise where the user has to describe the behavior of a given program. |
| `6` | OutputExercise | An exercise where the user has to describe the output which a given program produces. |
| `7` | ProgrammingExercise | An exercise where the user has to write a program which produces a desired output. |

## ExerciseLanguage

An enumeration to standardize the programming language used in an exercise. The languages are as follows:

| ID | Language | Description |
|---|---|---|
| `1` | Python | There is nothing much to say about Python; it's simply the best. |
| `2` | Java | Why does this abomination exist? |
