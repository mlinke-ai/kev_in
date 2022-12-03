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

The GET method os used to retrieve user data based on attributes.

### Access

Python `requests`:

```python
requests.request("GET", "http://<address>:<port>/user", json=<arguments>, headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl -X GET -d '<arguments>' -H "Content-Type: application/json" http://<address>:<port>/user
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/user", {method: "GET", headers: {"Content-Type": "application/json"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `user_id` | `int` | optional | `1` | The ID of the user. Normally obtained after creating a new user or logging in an existing user |
| `user_name` | `string` | optional | `John Doe` | The name of the user. Uniqueness is not guaranteed. |
| `user_pass` | `string` | optional | `b94d27b9934d3e08a...` | The SHA256 hash of the user password as defined in FIPS 180-2. |
| `user_mail` | `string` | optional | `john.doe@example.com` | The e-mail address of the user. |

Arguments are constructed as dictionaries or JSON objects.

### Response

The response is a dictionary or JSON object. The user ID is mapped to all user attributes except `user_pass` which is omitted.

```
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
