---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2022-01-10
---

# Exercise API

The exercise route is the endpoint to perform all different kinds of operations on the exercise database.

The endpoint can be accessed at `<address>:<port>/exercise`.

This endpoint is only accessible if the client is logged in as a existing user (if he sends the session cookie with a JWT inside).

## GET

The GET method is used to retrieve exercise data based on attributes. This method supports paging. Paging prevents overwhelming the API by reducing the number of returned elements. When a request is expected to return a huge number of elements, one can reduce the number of elements with the `exercise_offset` and `exercise_limit` arguments. `exercise_offset` defines the lowest `exercise_id` while `exercise_limit` defines the number of elements in the page. The default value for `exercise_limit` is defined in `config.MAX_ITEMS_RETURNED`. To get all values, simply execute multiple requests with adjusted values for `exercise_offset`. If `exercise_id` is provided `exercise_offset` and `exercise_limit` get ignored.

### Access

Python `requests`:

```python
requests.request("GET", "http://<address>:<port>/exercise?<URLarguments>")
```

Unix `curl`:

```
curl --location --request GET 'http://<address>:<port>/exercise?<URLarguments>'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/exercise?<URLarguments>", {method: "GET"})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<URLarguments>` with key value pairs in the form `key=value`(key is the argument, example values are listed in the table below). Multiple arguments are separated with `&`.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `exercise_id` | `int` | optional | `1` | The ID of the exercise. Normally obtained after creating a new exercise. This argument can be provided multiple times to select multiple exercises. All other arguments still apply.|
| `exercise_title` | `string` | optional | `My Exercise` | The display title of the exercise. |
| `exercise_description` | `string` | optional | `This is a good Test example!` | The description of the exercise
| `exercise_type` | `int` | optional | `2` | The type of the exercise: `1` for GapTextExercise, `2` for SyntaxExercise, `3` for ParsonsPuzzleExercise, `4` for FindTheBugExercise, `5` for DocumentationExercise, `6` for OutputExercise, `7` for ProgrammingExercise|
| `exercise_content` | `dict` | optional | `{"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}` | A JSON dict or object, containing the content of the exercise. The encoding is `exercise_type`-specific. |
| `exercise_page` | `int` | optional | `1` | The page of the query result. Default value is 1. |
| `exercise_limit` | `int` | optional | `1` | The size of a page. If a page is requested and `user_limit` is not set `config.MAX_ITEMS_RETURNED` gets used as default value. |
| `exercise_language` | `int` | optional | `Python` | Programming Language of the exercise. `1` for Python, `2` for Java |
| `exercise_details` | `bool` | optional | `true` | Query the system for advanced exercise details. |
| `exercise_solution` | `dict` | optional | `{"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}` | A JSON object or dict, containing the solution of the exercise. The encoding is `exercise_type`-specific. |

Arguments are constructed as dictionaries or JSON objects.

### Response

NOTE: It is possible that the system returns up to `Config.MAX_ITEMS_RETURNED` items.

=== "200"

    The response is a dictionary of JSON object. `"data"` is mapped to the query result as a list. `"meta"` is mapped to the meta data.

    Response structure:
    | Field | Description |
    |:--|:--|
    | `"data"` | A list of the elements returned by the query ordered by `exercise_id`. |
    | `"next_page"` | The index of the next page. If there is no next page this value will be `null`. |
    | `"next_url"` | The URL to request the next page. If there is no next page this value will be `null`. |
    | `"page_size"` | The number of elements in the current page. |
    | `"pages"` | The number of pages. |
    | `"prev_page"` | The index of the previous page. If the is no previous page this value will be `null`. |
    | `"prev_url"` | The URL to request the previous page. If there is no previous page this value will be `null`. |
    | `"total"` | The total number of elements which match the query. Basically the sum of all page sizes. |

    ```JSON
    {
        "data": [
            {
                "exercise_id": 70,
                "exercise_language_name": "Python",
                "exercise_language_value": 1,
                "exercise_title": "ProgrammingExercise9",
                "exercise_type_name": "ProgrammingExercise",
                "exercise_type_value": 7
            }
        ],
        "meta": {
            "next_page": null,
            "next_url": null,
            "page_size": 1,
            "pages": 1,
            "prev_page": null,
            "prev_url": null,
            "total": 1
        }
    }
    ```

=== "204"

	The database query yielded no results with the given parameters. The response body is empty.

=== "400"

	The `exercise_limit` is out of range, e.g. grater then `config.MAX_ITEMS_RETURNED`.

	```JSON
	{
		"message": "Page limit not in range",
		"min_limit": "<min_value>",
		"max_limit": "<max_value>"
	}
	```

=== "401"

    No session cookie was provided.

    ```JSON
    {
        "message": "Login required"
    }
    ```

=== "403"

    An unauthorized client sent a request.

    ```JSON
    {
        "message": "No Access"
    }
    ```

## POST

The post method is used to create new exercises.

### Access

This method is usable for all admins.

Python `requests`:

```python
requests.request("POST", "http://<address>:<port>/exercise", json=<arguments>, headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl --location --request POST 'http://<address>:<port>/exercise' \
--header 'Content-Type: application/json' \
--data-raw '{
    <arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/exercise", {method: "POST", headers={"Content-Type": "application/json"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below. (in curl in key value pairs `"<key>": "<value>"`)

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `exercise_title` | `string` | required | `My Exercise` | The display title of the exercise. |
| `exercise_description` | `string` | required | `This is a good Test example!` | The description of the exercise
| `exercise_type` | `int` | required | `1` | Number between 1 and 7 for the different exercise types, as defined in the database model. |
| `exercise_content` | `dict` | required | `{"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}` | A JSON dict or object, containing the content of the exercise. The encoding is `exercise_type`-specific. |
| `exercise_language` | `int` | required | `Python` | Programming Language of the exercise. `1` for Python, `2` for Java |
| `exercise_solution` | `dict` | required | `{"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}` | A JSON object or dict, containing the solution of the exercise. The encoding is `exercise_type`-specific. |

Arguments are constructed as dictionaries or JSON objects.

### Response

=== "201"

    The response is a dictionary or JSON object, Together with HTTP status 201. All attributes of the created exercise will be shown, together with a response message.

    ```JSON
    {
        "exercise_content": {
            "list": [
                "Hello",
                "this",
                "World",
                "is",
                "the",
                "first",
                "exercise"
            ]
        },
        "exercise_description": "This is a good Test example!",
        "exercise_id": 71,
        "exercise_title": "MyExercise2",
        "message": "The exercise was created successfully"
    }
    ```

=== "400"

    A required argument was not send.

    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```

=== "401"

    No session cookie was provided.

    ```JSON
    {
        "message": "Login required"
    }
    ```

=== "403"

    An unauthorized client sent a request.

    ```JSON
    {
        "message": "No Access"
    }
    ```

=== "409"

    An exercise with the given `exercise_title` already exists.

    ```JSON
    {
        "message": "An exercise with this title already exists"
    }
    ```

=== "500"

    The element could not be added to the database for some reason.

    ```JSON
    {
        "message": "An error occurred while creating the exercise"
    }
    ```

## PUT

The put method is used to change arguments from an exercise.

### Access

This method is usable for all admins.

Python `requests`:

```python
requests.request("PUT", "http://<address>:<port>/exercise", json=<arguments>, headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl --location --request PUT 'http://<address>:<port>/exercise' \
--header 'Content-Type: application/json' \
--data-raw '{
    <arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/exercise", {method: "PUT", headers={"Content-Type": "application/json", "Cookie": "token=<token>"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below. (in curl in key value pairs `"<key>": "<value>"`)

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `exercise_id` | `int` | required | `1` | The ID of the exercise. Normally obtained after creating a new exercise. |
| `exercise_title` | `string` | optional | `My Exercise` | The display title of the exercise. |
| `exercise_description` | `string` | optional | `This is a good Test example!` | The description of the exercise
| `exercise_type` | `int` | optional | `1` | Number between 1 and 7 for the different exercise types, as defined in the database model. |

Arguments are constructed as dictionaries or JSON objects.

### Response

=== "200"

    The response is a dictionary or JSON object, together with HTTP status 200. The response is a message.

    ```JSON
    {
        "message": "Successfully changed exercise with exercise_id 1"
    }
    ```

=== "400"

    A required argument was not sent.

    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```

=== "401"

    No session cookie was provided.

    ```JSON
    {
        "message": "Login required"
    }
    ```

=== "403"

    An unauthorized client sent a request.

    ```JSON
    {
        "message": "No Access"
    }
    ```

=== "404"

    No exercise with the given `exercise_id` exists.

    ```JSON
    {
        "message": "Exercise with exercise_id 1 does not exist"
    }
    ```

## DELETE

The delete method is used to delete an existing exercise.

### Access

This method is usable for all admins.

Python `requests`:

```python
requests.request("DELETE", "http://<address>:<port>/exercise", json=<arguments>, headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl --location --request DELETE 'http://<address>:<port>/exercise' \
--header 'Content-Type: application/json' \
--data-raw '{
    <arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/exercise", {method: "DELETE", headers={"Content-Type": "application/json"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below. (in curl in key value pairs `"<key>": "<value>"`)

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `exercise_id` | `int` | required | `1` | The ID of the exercise. Normally obtained after creating a new exercise. |

Arguments are constructed as dictionaries or JSON objects.

### Response

=== "200"

    The response is a dictionary or JSON object, Together with HTTP status 200. The response is a message.

    ```JSON
    {
        "message": "Successfully deleted exercise with exercise_id 1"
    }
    ```

=== "400"

    A required argument was not sent.

    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```

=== "401"

    No session cookie was provided.

    ```JSON
    {
        "message": "Login required"
    }
    ```

=== "403"

    An unauthorized client senT a request.

    ```JSON
    {
        "message": "No Access"
    }
    ```

=== "400"

    No exercise with the given `exercise_id` exists.

    ```JSON
    {
        "message": "Exercise with exercise_id 1 does not exist"
    }
    ```
