# Testing

## Exercise tests

## Login tests

## Solution tests

## User tests

### GET tests

#### `test_get_existing_by_id`

- tests whether the system finds and returns an existing user correctly based on the users ID
- input: HTTP request with `user_id = 2`
- expected output: `{"user_id":2,"user_name":"tuser","user_mail":"tuser@example.com","user_role":"User"}` and HTTP status `200`

#### `test_get_existing_by_name`

- tests whether the system finds and returns an existing user correctly based on the users name
- input: HTTP request with `user_name = "tuser"`
- expected output: `{"user_id":2,"user_name":"tuser","user_mail":"tuser@example.com","user_role":"User"}` and HTTP status `200`

#### `test_get_existing_by_mail`

- tests whether the system finds and returns an existing user correctly based on the users mail address
- input: HTTP request with `user_mail = "tuser@example.com"`
- expected output: `{"user_id":2,"user_name":"tuser","user_mail":"tuser@example.com","user_role":"User"}` and HTTP status `200`

#### `test_get_existing_by_role`

- tests whether the system finds and returns an existing user correctly based on the users role
- input: HTTP request with `user_role = 3`
- expected output: `{"user_id":2,"user_name":"tuser","user_mail":"tuser@example.com","user_role":"User"}` and HTTP status `200`

#### `test_get_non_existing_by_id`

- tests how the system handles an request with an ID wich is not present in the database
- input: HTTP request with `user_id = 25`
- expected output: `{}` and HTTP status `200`

#### `test_get_non_existing_by_name`

- tests how the system handles an request with a name which is not present in the database
- input: HTTP request with `user_name = "nuser"`
- expected output: `{}` and HTTP status `200`

#### `test_get_non_existing_by_mail`

- tests how the system handles an request with a mail address which is not present in the database
- input: HTTP request with `user_mail = "nuser@example.com"`
- expected output: `{}` and HTTP status `200`

#### `test_get_non_existing_by_role`

- tests how the system handles an request with a role which is not present in the database
- input: HTTP request with `user_role = 4`
- expected output: `{"message":{"user_role":"4 is not a valid UserRole}}` and HTTP status `400`

#### `test_restrict_page_size`

- tests whether the system correctly returns only the amount of elements which is specified in `user_limit` parameter
- input: HTTP request with `user_limit = 5`
- expected output: response contains exactly 5 users and HTTP status `200`

### POST tests

#### `test_create_user`

- tests whether the system correctly creates a new user
- input: HTTP request with `{"user_name": "Josslin Aloj", "user_mail": "Josslin.Aloj@example.com", "user_pass": "ian80"}`
- expected output: `{"message":"The user was created successfully", "user_name": "Josslin Aloj", "user_mail": "Josslin.Aloj@example.com", "user_pass": "ian80"}` and HTTP status `201`

#### `test_create_admin`

- tests whether the system correctly creates a new admin
- input: HTTP request with `{"user_name": "Thurmon Uli","user_mail": "Thurmon.Uli@example.com","user_pass": "Pi5ta","user_role": 2}`
- expected output: `{"user_name": "Thurmon Uli","user_mail": "Thurmon.Uli@example.com","user_pass": "Pi5ta","user_role": 2,}` and HTTP status `201`

#### `test_create_user_without_token`

- tests whether it is possible to create a user with out a token (without being logged in)
- necessary to allow new users to create a account (they don't have a login yet, so they can't request a token)
- input: HTTP request with `{"user_name": "Kon Archy", "user_mail": "Kon.Archy@example.com", "user_pass": "Fip5k"}`
- expected output: `{"message":"The user was created successfully","user_name": "Kon Archy", "user_mail": "Kon.Archy@example.com", "user_pass": "Fip5k"}` and HTTP status `201`

#### `test_create_admin_without_token`

- tests whether the system rejects the attempt to create an admin without any token
- input: HTTP request with `{"user_name": "Detleff Deric","user_mail": "Detleff.Deric@example.com","user_pass": "eNg9h","user_role": 2}`
- expected output: `{"message":"Login required"}` and HTTP status `401`

#### `test_create_admin_with_user_token`

- tests whether the system rejects the attempt to create an admin without being the SAdmin (the SAdmin token is send in the request header)
- input: HTTP request with `{"user_name": "Eldrige Ernesto","user_mail": "Eldrige.Ernesto@example.com","user_pass": "Xah8e","user_role": 2}`
- expected output: `{"message":"No Access"}` and HTTP status `403`

#### `test_create_duplicate_user`

- tests whether the system rejects a new user with an existing mail (mail addresses have to be unique system wide)
- input: two HTTP requests with `{"user_name": "Geoffrey Tretan", "user_mail": "Geoffrey.Tretan@example.com", "user_pass": "Abeo0"}`
- expected output: `{"message":"A user with this mail already exists"}` and HTTP status `409`

#### `test_create_user_with_empty_name`

- tests whether the system rejects the attempt to create an account with an empty name
- input: HTTP request with `{"user_name": "", "user_mail": "Gofried.Dietbald@example.com", "user_pass": "koh6P"}`
- expected output: `{"message":"user_name must not be empty"}` and HTTP status `400`

#### `test_create_user_with_empty_mail`

- tests whether the system rejects the attempt to create an account with an empty mail
- input: HTTP request with `{"user_name": "Rane Loewe", "user_mail": "", "user_pass": "Lohw3"}`
- expected output:`{"message":"user_mail must not be empty"}` and HTTP status `400`

#### `test_create_user_with_empty_password`

- tests whether the system rejects the attempt to create an account with an empty password
- input: HTTP request with `{"user_name": "Pepin Kuefer", "user_mail": "Pepin.Kuefer@example.com", "user_pass": ""}`
- expected output:`{"message":"user_pass must not be empty"}` and HTTP status `400`

#### `test_create_user_with_long_name`

- tests whether the system can handle a long name
- `<long_name>` is a string of 1024 random characters
- input: HTTP request with `{"user_name": <long_name>, "user_mail": "long.mail@example.com", "user_pass": "Eiph9"}`
- expected output: `{"user_name": <long_name>, "user_mail": "long.mail@example.com"}` and HTTP status `201`

#### `test_create_user_with_strange_name`

- tests whether the system can handle strange names consisting of unicode characters
- `<strange_name>` is a string of 14 unicode characters
- input: HTTP request with `{"user_name": <strange_name>, "user_mail": "strange.mail@example.com", "user_pass": "ai2Ou"}`
- expected output: `{"user_name": <strange_name>, "user_mail": "strange.mail@example.com",}` and HTTP status `201`

### PUT tests

#### `test_change_mail_to_existing`

- tests whether the system rejects the attempt to change the mail to an already existing one
- input: HTTP request with `"user_mail": "double.mail@example.com"`
- expected output: `{"message":"A user with this mail already exists"}` and HTTP status `409`

#### `test_change_to_empty_name`

- tests whether the system rejects the attempt to change to an empty name
- input: HTTP request with `"user_name":""`
- expected output: `{"message":"user_name must no be empty"}` and HTTP status `400`

#### `test_change_to_empty_mail`

- tests whether the system rejects the attempt to change to an empty mail
- input: HTTP request with `"user_mail":""`
- expected output: `{"message":"user_mail must not be empty"}` and HTTP status `400`

#### `test_change_to_empty_password`

- tests whether the system rejects the attempt to change to an empty pass
- input: HTTP request with `"user_pass":""`
- expected output: `{"message":"user_pass must not be empty"}` and HTTP status `400`

#### `test_change_admin_elevation`

- tests whether the system rejects the attempt to raise the user role to Admin without a SAdmin token
- input HTTP request with `"user_role":2` but no SAdmin token in header
- expected output: `{"message":"No Access"}` and HTTP status `403`

#### `test_change_sadmin_elevation`

- tests whether the system rejects the attempt to raise the user role to SAdmin without a SAdmin token
- input: HTTP request with `"user_role":1` but no SAdmin token in header
- expected output: `{"message":"No Access"}` and HTTP status `403`

### DELETE tests

#### `test_delete_existing`

- tests whether the system correctly deletes an existing user
- input: HTTP request with a previously created used ID
- expected output: `{"message":"Successfully deleted user with user_id <user_id>"}` and HTTP status `200`

#### `test_delete_non_existing`

- tests whether the system handles deleting a non existing user
- input: HTTP request whit a user ID which does not exist
- expected output: `{"message":"User with user_id <user_id> does not exist"}` and HTTP status `404`

#### `test_delete_self_as_admin`

- tests whether a request with an admin token can delete an admin account
- input: HTTP request with admin token
- expected output: `{"message":"Successfully deleted user with user_id <user_id>}` and HTTP status `200`

#### `test_delete_self_as_user`

- tests whether a request with a user token can delete the account associated with the token
- input: HTTP request with user token
- expected output: `{"message":"Successfully deleted user with user_id <user_id>"}` and HTTP status `200`

#### `test_delete_other_as_admin`

- tests whether a request with an admin token can delete another account
- input: HTTP request with admin token
- expected output: `{"message":"Successfully deleted user with user_id <user_id>"}` and HTTP status `200`

#### `test_delete_other_as_user`

- tests whether the system rejects the attempt of a request with a user token to delete another account
- input: HTTP request with user token
- expected output: `{"message":"No Access}` and HTTP status `403`
