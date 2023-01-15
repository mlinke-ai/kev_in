import requests

# sign up
r = requests.request("POST", "http://127.0.0.1:5000/user", json={"user_name": "test_user", "user_pass": "12341234",
                     "user_mail": "test@example.com", "user_role": 3}, headers={"Content-Type": "application/json"})
print(r.status_code)

# sign in
r = requests.request("POST", "http://127.0.0.1:5000/login", json={
                     "user_name": "sadmin", "user_pass": "sadmin"}, headers={"Content-Type": "application/json"})
token = r.cookies.get("token")
print(r.status_code)

# create an ParsonsPuzzleExercise
r = requests.request(
  "POST",
  "http://127.0.0.1:5000/exercise",
  json={"exercise_title": "Solve the Puzzle", "exercise_description":
        "Place the items in the correct order!", "exercise_type": 3, "exercise_content": "1-print(123) 2-return0"},
  headers={"Content-Type": "application/json",
            "Cookie": "token="+token},
)
print(r.status_code)

# retrieve an ParsonsPuzzleExercise -> works only with the exercise id =(
r = requests.request(
  "GET",
  "http://127.0.0.1:5000/exercise",
  json= {"exercise_title": "Solve the Puzzle"},
  headers={"Content-Type": "application/json", "Cookie": "token="+token})

print(r.status_code, r.content)
