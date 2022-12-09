---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2022-12-09
---

# Login API

The login route is the enpoint to perform the login authentication process. After the login is performed the client gets a JWT (JSON Web Token) which it has to store and which it can use to authenticate against the server. 

After the login Process is done the client has to send the JWT with every following HTTP-request as a header `Authorization: Bearer <token>` until logging out.

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

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `user_name` | `string` | required | `John Doe` | The name of the user. |
| `user_pass` | `string` | required | `b94d27b9934d3e08a...` | The SHA256 hash of the user password as defined in FIPS 180-2. |

Arguments are constructed as dictionaries or JSON objects.

### Response

The response is a dictionary or JSON object. If authentication process succeeds the JWT (JSON Web Token) is returned. Otherwise an error message will be returned.

```
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.HFnoe0RmWao72CHwfjaaUHPmXs8QW8jPL_vXfmHIH38"
}
```
```
{
    "message": "Incorrect user name or password"
}
```