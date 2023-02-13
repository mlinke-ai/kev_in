import requests

# # sign up
# r = requests.request("POST", "http://127.0.0.1:5000/user", json={"user_name": "test_user", "user_pass": "12341234",
#                      "user_mail": "test@example.com", "user_role": 3}, headers={"Content-Type": "application/json"})
# print(r.status_code)

# sign in as admin
r = requests.request("POST", "http://127.0.0.1:5000/login", json={
                     "user_mail": "sadmin@example.com", "user_pass": "sadmin"}, headers={"Content-Type": "application/json"})
token = r.cookies.get("token")
print("sadmin login: ", r.status_code)

# delete an ParsonsPuzzleExercise
r = requests.request(
  "DELETE",
  "http://127.0.0.1:5000/exercise",
  json={
    "exercise_id": 1,
  },
  headers={
    "Content-Type": "application/json",
    "Cookie": "token="+token
  },
)
print("delete ppe: ", r.status_code)

# # create an ParsonsPuzzleExercise
# r = requests.request(
#   "POST",
#   "http://127.0.0.1:5000/exercise",
#   json={
#     "exercise_title": "hallo",
#     "exercise_description": "Place the items in the correct order!",
#     "exercise_type": 3,
#     "exercise_content": "[{id: 1, name: import math}, {id: 2, name: print (math.pi)}]",
#     "exercise_solution": "[{id: 1, name: import math}, {id: 2, name: print (math.pi)}]",
#     "exercise_language": 1
#   },
#   headers={
#     "Content-Type": "application/json",
#     "Cookie": "token="+token
#   },
# )
# print("ppe creation: ", r.status_code)

# retrieve an ParsonsPuzzleExercise
r = requests.request(
  "GET",
  "http://127.0.0.1:5000/exercise?exercise_type=3&exercise_details=true",
  headers={"Content-Type": "application/json", "Cookie": "token="+token})

print("retrieve ppe: ", r.status_code, r.content)
