---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2022-01-10
---

# User API
  
The user route is the endpoint to perform all different kinds of operations on the user database.
The endpoint can be accessed at `<address>:<port>/user`.

## GET

The GET method is used to retrieve user data based on attributes. This method supports paging. Paging prevents overwhelming the API by reducing the number of returned elements. When a request is expected to return a huge number of elements, one can reduce the number of elements with the `user_offset` and `user_limit` arguments. `user_offset` defines the lowest `user_id` while `user_limit` defines the number of elements in the page. The default value for `user_limit` is defined in `config.MAX_ITEMS_RETURNED`. To get all values, simply execute multiple requests with adjusted values for `user_offset`. If `user_id` is provided `user_offset` and `user_limit` get ignored.

### Access

Python `requests`:  

```python
requests.request("GET", "http://<address>:<port>/user?<URLarguments>")
```

Unix `curl`:

```
curl --location --request GET 'http://<address>:<port>/user?<URLarguments>'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/user?<URLarguments>", {method: "GET"})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<URLarguments>` with key value pairs in the form `key=value`(key is the argument, example values are listed in the table below). Multiple arguments are seperated with `&`.

### Arguments

Arguments are constructed as dictionaries or JSON objects.

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `user_id` | `int` | optional | `1` | The ID of the user. Normally obtained after creating a new user. |
| `user_name` | `string` | optional | `John Doe` | The name of the user. Uniqueness is not guaranteed. |
| `user_mail` | `string` | optional | `john.doe@example.com` | The e-mail address of the user. This is unique for every account. |
| `user_role` | `int` | optional  | `1` | An integer defining the user role. One of the following values: `1` for super admin, `2` for admin and `3` for regular users. |
| `user_offset` | `int` | optional | `1` | The lowest index to return when a page is requested. |
| `user_limit` | `int` | optional | `1` | The size of a page. If a page is requested and `user_limit` is not set `config.MAX_ITEMS_RETURNED` gets used as default value. |

Note: If no argument is sent, the system returns the user data of the logged in client (not as dict).

### Response

NOTE: It is possible that the system returns up to `Config.MAX_ITEMS_RETURNED` items.

=== "200"

	The response is a dictionary of JSON object. The user ID is mapped to all user attributes.

	```JSON
	{
		"1": {
			"user_id": 1,
			"user_name": "John Doe",
			"user_mail": "john.doe@example.com",
			"user_role": "User"
		}
	}
	```

=== "400"

	The `user_limit` is out of ragne, e.g. grater then `config.MAX_ITEMS_RETURNED`.

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

	An unauthorized client send a request.

	```JSON
	{
		"message": "No Access"
	}
	```

If no argument is sent the reponse is not mapped to the `user_id`:

	```JSON
	{
		"user_id": 1,
		"user_name": "John Doe",
		"user_mail": "john.doe@example.com",
		"user_role": "User"
	}
	```

## POST

The POST method is used to create a new user. 
This method prevents duplication.

### Access

No Authorizazion is needed. So this method can be accessed without sending a cookie.

Python `requests`:  

```python
requests.request("POST", "http://<address>:<port>/user",json=<arguments>,headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl --location --request POST 'http://<adress>:<port>/user' \
--header 'Content-Type: application/json' \
--data-raw '{
	<arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/user", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below. (in curl in key value pairs `"<key>": "<value>"`)

### Arguments

| Argument | Type | Necessity | Example | Description |
|---|---|---|---|---|
| `user_name` | `string` | required | `John Doe` | The name of the user. Uniqueness is guaranteed. |
| `user_pass` | `int` | required | `testPW` | The password of the new user. |
| `user_mail` | `string` | required | `john.doe@example.com` | The e-mail address of the user. This is unique for every account. |

### Response

=== "201"

	The response is a dictionary or JSON object, Together with HTTP status 201. New user's name and id will be returned, together with a response message.

	```JSON
	{
		"message": "The user was created successfully",
		"user_name": "John Doe",
		"user_id": 1
	}
	```

=== "409"

	The request contains already existing user name or email.

	```JSON
	{
		"message": "A user with this name already exists"
	}
	```

=== "500"

	The user could not be added to the database for some reason.

	```JSON
	{
		"message": "An error occurred while creating the user"
	}
	```

## PUT

### Access

Python `requests`:

```python
requests.request("PUT", "http://<address>:<port>/exercise", json=<arguments>, headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl --location --request PUT 'http://<adress>:<port>/user' \
--header 'Content-Type: application/json' \
--data-raw '{
	<arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/user", {method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below. (in curl in key value pairs `"<key>": "<value>"`)

**TODO: Arguments and response**

## DELETE

### Access

Python `requests`:

```python
requests.request("DELETE", "http://<address>:<port>/exercise", json=<arguments>, headers={"Content-Type": "application/json"})
```

Unix `curl`:

```
curl --location --request PUT 'http://<adress>:<port>/user' \
--header 'Content-Type: application/json' \
--data-raw '{
	<arguments>
}'
```

JavaScript `fetch`:

```javascript
fetch("http://<address>:<port>/user", {method: "DELETE", headers: {"Content-Type": "application/json"}, body: JSON.stringify(<arguments>)})
```

Replace `<address>` and `<port>` with your respective setup.
Replace `<arguments>` with the arguments listed below. (in curl in key value pairs `"<key>": "<value>"`)

**TODO: Arguments and response**