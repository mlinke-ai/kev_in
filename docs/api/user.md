---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2022-11-26
---

# User API

The user route is the endpoint to perform all different kinds of operations on the user database.

The endpoint can be accessed at `<address>:<port>/user`.

!!! danger "Authentication!"
    Currently there is no request authentication!

## GET

The GET method is used to retrieve user data based on attributes.

### Access

Python `requests`:

```python
requests.request("GET", "http://<address>:<port>/user?<arguments>", headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl --location --request GET 'http://<adress>:<port>/user?<arguments>' \
--header 'Content-Type: application/json' \
--data-raw ''
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/user?<arguments>", {method: "GET", headers: {"Content-Type": "application/json"}})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with with key value pairs in the form `key=value` (key is the argument, example values are listed in the table below). If you want to pass multiple arguments you can pass them like this `<argument1>&<argument2>`.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `user_id` | `int` | optional | `1` | The ID of the user. Normally obtained after creating a new user. |
| `user_name` | `string` | optional | `John Doe` | The name of the user. Uniqueness is not guaranteed. |
| `user_mail` | `string` | optional | `john.doe@example.com` | The e-mail address of the user. |

Arguments are constructed as dictionaries or JSON objects.

### Response

The response is a dictionary or JSON object. The user ID is mapped to all user attributes.

```JSON
{
  "1": {
    "user_id": 1,
    "user_name": "John Doe",
    "user_mail": "john.doe@example.com"
  }
}
```

## POST

## PUT

## DELETE
