---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2023-01-04
---

# Solution API

The solution route is the endpoint to perform all different kinds of operations on the solution database.

The endpoint can be accessed at `<address>:<port>/solution`.

## GET

The GET method is used to retrieve solution data based on attributes. This Method supports paging. Paging prevents overwhelming the API by reducing the number of returned elements. When a request is expected to return a huge number of elements, one can reduce the number of elements with the `solution_offset` and `solution_limit` arguments. `solution_offset` defines the lowest `solution_id` while `solution_limit` defines the number of elements in the page. The default value for `solution_limit` is defined in `config.MAX_ITEMS_RETURNED`. To get all values, simply execute multiple requests with adjusted values for `solution_offset`. If `solution_id` is provided `solution_offset` and `solution_limit` get ignored.

### Access

Python `requests`:

```python
requests.request("GET", "http://<address>:<port>/solution?<URLarguments>")
```

Unix `curl`:

```
curl --location --request GET 'http://<address>:<port>/solution?<URLarguments>'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/solution?<URLarguments>", {method: "GET"})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<URLarguments>` with key value pairs in the form `key=value`(key is the argument, example values are listed in the table below). Multiple arguments are separated with `&`.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `solution_id` | `int` | optional | `1` | The ID of the solution. Normally obtained after creating a new solution. |
| `solution_user` | `int` | optional | `1` | The ID of the user who provided the solution. |
| `solution_exercise` | `int` | optional | `1` | The ID of the exercise which the solution was provided for. |
| `solution_date` | `int` | optional | `1672946590` | The date and time when the solution attempt was started. Encoded as Unix timestamp. As querring for a specific timestamp, the system queries for all solutions which have the same year, month and date `solution_date`. |
| `solution_duration` | `int` | optional | `524` | The time the user needed to solve the exercise. Encoded in seconds. |
| `solution_correct` | `bool` | optional | `true` | Whether the solution solves the exercise correctly or not. |
| `solution_pending` | `bool` | optional | `false` | Whether the solution is in pending state. Pending state means an admin needs to evaluate the solution. |
| `solution_content` | `str` | optional | `"hello, world"` | The content provided by the user. Querring for the solution content is quite useless but this field is added for completeness. |
| `solution_offset` | `int` | optional | `1` | The lowest index to return when a page is requested. |
| `solution_limit` | `int` | optional | `1` | The size of the page. If a page is requested and `solution_limit` is not set `config.MAX_ITEMS_RETURNED` gets used as default value. |

### Response

NOTE: It is possible that the system returns up to `Config.MAX_ITEMS_RETURNED` items.

=== "200"

    The response is a dictionary of JSON object. The solution ID is mapped to all solution attributes.
    ```JSON
    {
        "2": {
            "solution_correct": true,
            "solution_date": "2023-01-11 15:16:25",
            "solution_duration": "122 days, 0:00:00",
            "solution_exercise": 1,
            "solution_id": 2,
            "solution_user": 1,
            "solution_pending": false,
            "solution_content": <...>
        }
    }
    ```

=== "400"

	The `user_limit` is out of range, e.g. grater then `config.MAX_ITEMS_RETURNED`.
	```JSON
	{
		"message": "Page limit not in range",
		"min_limit": <min_value>,
		"max_limit": <max_value>
	}
	```

=== "401"

    The request contains no cookie.
    ```JSON
    {
        "message": "Login required"
    }
    ```

=== "403"

    The cookie does not represent the necessary privileges. Mostly this is because a request with a user token tries to perform an admin only task.
    ```JSON
    {
        "message": "No Access"
    }
    ```

## POST

The post method is used to create new solutions.

### Access

Python `requests`:

```python
requests.request("POST", "http://<address>:<post>/solution", json=<arguments>, headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl --location --request GET 'http://<address>:<port>/solution' \
--header 'Content-Type: application/json' \
--header 'Cookie: token=<token>' \
--data-raw '{
    <arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/solution", {method: "POST", headers={"Content-Type": "application/json", "Cookie": "token=<token>"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup. Replace `<arguments>` with the arguments listed below. The structure is a dictionary or JSON object. Replace `<token>` with the JWT.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `solution_exercise` | `int` | required | `1` | The ID of the exercise which the solution was provided for. |
| `solution_date` | `int` | required | `1672946590` | The date and time when the solution attempt was started. Encoded as Unix timestamp. |
| `solution_duration` | `int` | required | `524` | The time the user needed to solve the exercise. Encoded in seconds. |
| `solution_content` | `str` | required | `"hello, world!"` | The content provided by the user. |

### Response

=== "201"

    The response is a dictionary or JSON object, together with the HTTP status 201. All attributes of the created exercise will be shown, together with a response message.
    ```JSON
    {
        "message": "Successfully submitted solution",
        "solution_correct": true,
        "solution_date": "2023-01-11 15:16:25",
        "solution_duration": "122 days, 0:00:00",
        "solution_exercise": 1,
        "solution_id": 2,
        "solution_user": 1,
        "solution_pending": false,
        "solution_content": <...>
    }
    ```

=== "400"

    If a required argument was not send:
    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```

=== "401"

    If no session cookie was provided:
    ```JSON
    {
        "message": "Login required"
    }
    ```

=== "403"

    If an unauthorized client sends a request:
    ```JSON
    {
        "message": "No Access"
    }
    ```

=== "500"

    If for some reason the element could not be added to the database:
    ```JSON
    {
        "message": "An error occurred while creating the solution"
    }
    ```

## PUT

The put method is used to change attributes of an existing solutions.

### Access

Python `requests`:

```python
requests.request("PUT", "http://<address>:<port>/solution", json=<arguments>, headers={"Content-Type": "application/json", "Cookie": "token=<token>"})
```

Unix `curl`:

```
curl --location --request PUT 'http://<address>:<port>/solution' \
--header 'Content-Type: application/json' \
--header 'Cookie: token=<token>' \
--data-raw '{
    <arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/solution", {method: "PUT", headers={"Content-Type": "application/json", "Cookie": "token=<token>"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup. Replace `<arguments>` with the arguments listed below. The structure is a dictionary or JSON object. Replace `<token>` with the JWT.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `solution_id` | `int` | required | `1` | The ID of the solution. Normally obtained after creating a new solution. |
| `solution_user` | `int` | optional | `1` | The ID of the user who provided the solution. |
| `solution_exercise` | `int` | optional | `1` | The ID of the exercise which the solution was provided for. |
| `solution_date` | `int` | optional | `1672946590` | The date and time when the solution attempt was started. Encoded as Unix timestamp. |
| `solution_duration` | `int` | optional | `524` | The time the user needed to solve the exercise. Encoded in seconds. |
| `solution_correct` | `bool` | optional | `true` | Whether the solution solves the exercise correctly or not. |
| `solution_pending` | `bool` | optional | `false` | Whether the solution is in pending state or not. |
| `solution_content` | `str` | optional | `"hello, world!"` | The content of the solution provided by the user. |

### Response

=== "200"

    The response is a dictionary or JSON object, together with HTTP status 200. The response contains a message.
    ```JSON
    {
        "message": "The solution with solution_id 1 was changed successfully."
    }
    ```

=== "400"

    If a required argument was not sent:
    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```

=== "401"

    If no session cookie was provided:
    ```JSON
    {
        "message": "Login required"
    }
    ```

=== "403"

    If an unauthorized client sent a request:
    ```JSON
    {
        "message": "No Access"
    }
    ```

=== "404"

    If no solution with the given `solution_id` exists:
    ```JSON
    {
        "message": "Solution with solution_id 1 does not exist"
    }

## DELETE

The delete method is used to delete an existing solution.

### Access

Python `requests`:

```python
requests.request("PUT", "http://<address>:<port>/solution", json=<arguments>, headers={"Content-Type": "application/json", "Cookie": "token=<token>"})
```

Unix `curl`:

```
curl --location --request PUT 'http://<address>:<port>/solution' \
--header 'Content-Type: application/json' \
--header 'Cookie: token=<token>' \
--data-raw '{
    <arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/solution", {method: "PUT", headers={"Content-Type": "application/json", "Cookie": "token=<token>"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup. Replace `<arguments>` with the arguments listed below. The structure is a dictionary or JSON object. Replace `<token>` with the JWT.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `solution_id` | `int` | required | `1` | The ID of the solution. Normally obtained after creating a new solution. |

### Response

=== "200"

    The response is a dictionary of JSON object, together with HTTP status 200. The response contains a message.
    ```JSON
    {
        "message": "The solution with the solution_id 1 was deleted successfully"
    }
    ```

=== "400"

    If a required argument was not sent:
    ```JSON
    {
        "message": {
            "argument": "Error Text"
        }
    }
    ```

=== "401"

    If no session cookie was provided:
    ```JSON
    {
        "message": "Login required"
    }
    ```

=== "403"

    If an unauthorized clients sends a request:
    ```JSON
    {
        "message": "No Access"
    }
    ```

=== "404"

    If no solution with the given `solution_id` exists:
    ```JSON
    {
        "message": "Solution with the solution_id 1 does no exist"
    }
    ```
