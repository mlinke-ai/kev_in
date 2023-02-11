---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2023-02-09
---

# Exercise Format Definitions
All exercise types define special data formats for the attributes `exercise_content`, `exercise_solution`
(ExerciseModel) and `solution_content` (SolutionModel). All definitions follow the JSON standard and are listed below.

## Parsons Puzzle Exercise
### exercise_content
```JSON
{
    "list": [
        "<piece 1>",
        "<piece 2>",
        ...
        "<piece n>"
    ]
}
```
**example:**
```JSON
"exercise_content": {
        "list": [
            "Hello",
            "World",
            "this",
            "is",
            "the",
            "first",
            "exercise"
        ]
    }
```
Note: When getting this via GET, the pieces will be randomized.

### exercise_solution
```JSON
{
    "list": [
        "<piece 1>",
        "<piece 2>",
        ...
        "<piece n>"
    ]
}
```
**example:**
```JSON
"exercise_solution": {
        "list": [
            "Hello",
            "World",
            "this",
            "is",
            "the",
            "first",
            "exercise"
        ]
    }
```

### solution_content
```JSON
{
    "list": [
        "<piece 1>",
        "<piece 2>",
        ...
        "<piece n>"
    ]
}
```
**example:**
```JSON
"solution_content": {
        "list": [
            "Hello",
            "World",
            "this",
            "is",
            "the",
            "first",
            "exercise"
        ]
    }
```

## Programming Exercise
### exercise_content

```JSON
{
    "code": "<sample_code>",
    "func": "<function_name>"
}
```
`<func_name>` must be the name of the function to be called from the evaluator

**example:**
```JSON
{
    "exercise_content": {
        "code": "def multiply(x,y):\r\npass",
        "func": "multiply"
    }
}
```

### exercise_solution

```JSON
{
    "0": [[<params>],[<result>]],
    "1": [[<params>],[<result>]],
    ...
    "n": [[<params>],[<result>]]
}
```
`params` should be a list of parameters, according to the expected data types of the executed function.
`result` should be the expected output of the function (should also be a list).

**example:**
```JSON
{
    "exercise_solution": {
        "0": [[0, 0], [0]],
        "1": [[1, 0], [0]],
        "2": [[1, 2], [2]],
        "3": [[2, 2], [4]],
        "4": [[6, 7], [42]],
        "5": [[-4, 5], [-20]],
    }
}
```

### solution_content
```JSON
{
    "code": "<user_code>"
}
```
`<user_code>` should be the code the user submits

**example:**
```JSON
{
    "solution_content": {
        "code": "def multiply(x,y):\r\nreturn x*y"
    }
}
```
