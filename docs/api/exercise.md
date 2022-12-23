---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2022-12-23
---

# Exercise API

The exercise route is the endpoint to perform all different kinds of operations on the exercise database.

The endpoint can be accessed at `<address>:<port>/exercise`.

This endpoint is only accessable if the client is logged in as a existing user (if he sends the session cookie with a JWT inside).

## GET

The GET method is used to get exercise data based on attributes.

### Access

This method is usable for all users.

Python `requests`:

```python
requests.request("GET", "http://<address>:<port>/exercise?<arguments>", headers={"Content-Type": "application/json", "Authorization": "Bearer <token>"})
```

Unix `curl`:

```
curl --location --request GET 'http://<address>:<port>/erxercise?<arguments>' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data-raw ''
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/exercise?<arguments>", {method: "GET", headers: {"Content-Type": "application/json", "Authorization": "Bearer <token>"}})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with with key value pairs in the form `key=value` (key is the argument, example values are listed in the table below). If you want to pass multiple arguments you can pass them like this `<argument1>&<argument2>`.
Replace `<token>` with the JWT.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `exercise_id` | `int` | required | `1` | The ID of the exercise. Normally obtained after creating a new exercise. |

Arguments are constructed as dictionaries or JSON objects.

### Response

The response is a dictionary or JSON object, Together with HTTP status 200. The exercise ID is mapped to all exercise attributes. If you pass `exercise_id = 0` then all existing exercises will be returned.

```JSON
{
    "1": {
        "exercise_content": "1+1=",
        "exercise_description": "This is a good Test example!",
        "exercise_id": 1,
        "exercise_title": "MyExercise",
        "exercise_type": "ExerciseType.ParsonsPuzzleExercise"
    }
}
```
`HTTP status 200`

### Fails

- if a required argument was not send:
    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```
    `HTTP status 400`

- If no session cookie was provided:
    ```JSON
    {
        "message": "Login required"
    }
    ```
    `HTTP status 401`

- If an unauthorized client sends a request:
    ```JSON
    {
        "message": "No Access"
    }
    ```
    `HTTP status 403`

## POST

The post method is used to create new exercises.

### Access

This method is usable for all admins.

Python `requests`:

```python
requests.request("POST", "http://<address>:<port>/exercise", json=<arguments>, headers={"Content-Type": "application/json", "Authorization": "Bearer <token>"})
```

Unix `curl`:

```
curl --location --request POST 'http://<address>:<port>/exercise' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data-raw '{
    <arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/exercise", {method: "POST", headers={"Content-Type": "application/json", "Authorization": "Bearer <token>"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below. (in curl in key value pairs `"<key>": "<value>"`)
Replace `<token>` with the JWT.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `exercise_title` | `string` | required | `My Exercise` | The display title of the exercise. |
| `exercise_description` | `string` | required | `This is a good Test example!` | The description of the exercise
| `exercise_type` | `int` | required | `1` | Number between 1 and 7 for the different exercise types, as defined in the database model. |
| `exercise_content` | `string` | required | `1+1=` | The content of the exercise. |

Arguments are constructed as dictionaries or JSON objects.

### Response

The response is a dictionary or JSON object, Together with HTTP status 201. All attributes of the created exercise will be shown, together with a response message.

```JSON
{
    "exercise_id": 1,
    "exercise_title": "My Exercise",
    "message": "The exercise was created successfully"
}
```
`HTTP status 201`

### Fails

- if a required argument was not send:
    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```
    `HTTP status 400`

- If no session cookie was provided:
    ```JSON
    {
        "message": "Login required"
    }
    ```
    `HTTP status 401`

- If an unauthorized client sends a request:
    ```JSON
    {
        "message": "No Access"
    }
    ```
    `HTTP status 403`

- If an exercise with the given `exercise_title` already exists:
    ```JSON
    {
        "message": "An exercise with this title already exists"
    }
    ```
    `HTTP status 409`

- If the element could not be added to the database for some reason:
    ```JSON
    {
    "message": "An error occurred while creating the exercise"
    }
    ```
    `HTTP status 500`

## PUT

The put method is used to change arguments from an exercise.

### Access

This method is usable for all admins.

Python `requests`:

```python
requests.request("PUT", "http://<address>:<port>/exercise", json=<arguments>, headers={"Content-Type": "application/json", "Authorization": "Bearer <token>"})
```

Unix `curl`:

```
curl --location --request POST 'http://<address>:<port>/exercise' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data-raw '{
    <arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/exercise", {method: "PUT", headers={"Content-Type": "application/json", "Authorization": "Bearer <token>"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below. (in curl in key value pairs `"<key>": "<value>"`)
Replace `<token>` with the JWT.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `exercise_id` | `int` | required | `1` | The ID of the exercise. Normally obtained after creating a new exercise. |
| `exercise_title` | `string` | optional | `My Exercise` | The display title of the exercise. |
| `exercise_description` | `string` | optional | `This is a good Test example!` | The description of the exercise
| `exercise_type` | `int` | optional | `1` | Number between 1 and 7 for the different exercise types, as defined in the database model. |
| `exercise_content` | `string` | optional | `1+1=` | The content of the exercise. |

Arguments are constructed as dictionaries or JSON objects.

### Response

The response is a dictionary or JSON object, Together with HTTP status 200. The response is a message.

```JSON
{
    "message": "Successfully chanaged exercise with exercise_id 1"
}
```
`HTTP status 200`

### Fails

- if a required argument was not send:
    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```
    `HTTP status 400`

- If no session cookie was provided:
    ```JSON
    {
        "message": "Login required"
    }
    ```
    `HTTP status 401`

- If an unauthorized client sends a request:
    ```JSON
    {
        "message": "No Access"
    }
    ```
    `HTTP status 403`

- If no exercise with the given `exercise_id` exists:
    ```JSON
    {
        "message": "Exercise with exercise_id 1 does not exist"
    }
    ```
    `HTTP status 404`

## DELETE

The delete method is used to delete an existing exercise.

### Access

This method is usable for all admins.

Python `requests`:

```python
requests.request("DELETE", "http://<address>:<port>/exercise", json=<arguments>, headers={"Content-Type": "application/json", "Authorization": "Bearer <token>"})
```

Unix `curl`:

```
curl --location --request POST 'http://<address>:<port>/exercise' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data-raw '{
    <arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/exercise", {method: "DELETE", headers={"Content-Type": "application/json", "Authorization": "Bearer <token>"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below. (in curl in key value pairs `"<key>": "<value>"`)
Replace `<token>` with the JWT.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `exercise_id` | `int` | required | `1` | The ID of the exercise. Normally obtained after creating a new exercise. |

Arguments are constructed as dictionaries or JSON objects.

### Response

The response is a dictionary or JSON object, Together with HTTP status 200. The response is a message.

```JSON
{
    "message": "Successfully deleted exercise with exercise_id 1"
}
```
`HTTP status 200`

### Fails

- if a required argument was not send:
    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```
    `HTTP status 400`

- If no session cookie was provided:
    ```JSON
    {
        "message": "Login required"
    }
    ```
    `HTTP status 401`

- If an unauthorized client sends a request:
    ```JSON
    {
        "message": "No Access"
    }
    ```
    `HTTP status 403`

- If no exercise with the given `exercise_id` or `exercise_title` exists:
    ```JSON
    {
        "message": "Exercise with exercise_id 1 does not exist"
    }
    ```
    `HTTP status 404`