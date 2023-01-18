---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2022-12-23
---

# Login API

The login route is the endpoint to perform the login authentication process. After the login is performed the client gets a session Cookie.

After the login Process is done the client has to send the session cookie with every HTTP request until logging out. (the cookie expires after one hour)

The endpoint can be accessed at `<address>:<port>/login`.

## POST

The POST method is used to perform the login. It is the only request-type supported by the login route.

### Access

Python `requests`:

```python
requests.request("POST", "http://<address>:<port>/login", json=<arguments>, headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl -X POST -d '<arguments>' -H "Content-Type: application/json" http://<address>:<port>/login
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/login", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below.

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `user_name` | `string` | required | `John Doe` | The name of the user. |
| `user_pass` | `string` | required | `testPW` | The user password as defined in the registration of the user account. |

Arguments are constructed as dictionaries or JSON objects.

### Response

=== "200"

    The response is a dictionary or JSON object. If authentication process succeeds a success message with a session cookie is returned with HTTP status 200.

    ```JSON
    {
        "message": "Welcome John Doe!"
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

    Password or username is incorrect.

    ```JSON
    {
        "message": "Incorrect user name or password"
    }
    ```