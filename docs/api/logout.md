---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2023-01-27
---

# Logout API

The logout route is to perform a logout. The session cookie will be deleted. 

The endpoint can be accessed at `<address>:<port>/logout`.

## POST

The POST method is used to perform the logout. It is the only request-type supported by the logout route.

### Access

Python `requests`:

```python
requests.request("POST", "http://<address>:<port>/logout")
```

Unix `curl`:

```
curl --location --request POST 'http://<address>:<port>/logout'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/logout", {method: "POST"})
```

Replace `<address>` and `<port>` with your respective setup.

### Arguments

No arguments are needed.

### Response

=== "200"

    Normally the response should be a 200 OK and a success message.
    It doesen't matter if the client was logged in before.

    ```JSON
    {
        "message": "Successfully logged out."
    }
    ```