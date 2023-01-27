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

## DELETE

The DELETE method is used to perform the logout. It is the only request-type supported by the logout route.

### Access

Python `requests`:

```python
requests.request("DELETE", "http://<address>:<port>/logout")
```

Unix `curl`:

```
curl --location --request DELETE 'http://<address>:<port>/logout'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/logout", {method: "DELETE"})
```

Replace `<address>` and `<port>` with your respective setup.

### Arguments

No arguments are needed.

### Response

=== "302"

    The response is an empty HTTP-response, containing a redirect to the base URL. HTTP status will be 302.