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

## GET

The GET method is used to retrieve user data based on attributes. This method supports paging. Paging prevents overwhelming the API by reducing the number of returned elements. When a request is expected to return a huge number of elements, one can reduce the number of elements with the `user_offset` and `user_limit` arguments. `user_offset` defines the lowest `user_id` while `user_limit` defines the number of elements in the page. The default value for `user_limit` is defined in `config.MAX_ITEMS_RETURNED`. To get all values, simply execute multiple requests with adjusted values for `user_offset`. If `user_id` is provided `user_offset` and `user_limit` get ignored.

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
Replace `<arguments>` with key value pairs in the form `key=value` (key is the argument, example values are listed in the table below). If you want to pass multiple arguments you can pass them like this `<argument1>&<argument2>`.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `user_id` | `int` | optional | `1` | The ID of the user. Normally obtained after creating a new user. |
| `user_name` | `string` | optional | `John Doe` | The name of the user. Uniqueness is not guaranteed. |
| `user_mail` | `string` | optional | `john.doe@example.com` | The e-mail address of the user. |
| `user_admin` | `bool` | optional | `true` | A flag whether the user is an admin or not. |
| `user_sadmin` | `bool` | optional | `false` | A flag whether the user is the super admin or not. |
| `user_offset` | `int` | optional | `1` | The lowest index to return when a page is requested. |
| `user_limit` | `int` | optional | `1` | The size of a page. If a page is requested and `user_limit` is not set `config.MAX_ITEMS_RETURNED` gets used as default value. |

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
