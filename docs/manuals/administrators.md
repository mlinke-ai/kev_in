---
title: Kev.in
summary: A learning platform form programming beginners.
authors:
    - Max Linke
    - and others
date: 2023-03-10
---

# Administrator manual

## Log-In
If you are on the starting page click on the `START NOW` button to log in an
existing account or to create a new one. By default the database provides two
accounts: tuser and sadmin (credentials of sadmin can be found in the
documentation in api/config). Since our Log in system works with cookies, you're
able to stay logged in even if you close your browser (the cookie disappears
after one hour inaktivity).

## Admin Dashboard
If you successfully logged in, you should see the admin dashboard. You might need 
to reload the page to be able to scroll. On the top right you can see the your 
username. By clicking on that, a dropdown menu opens where you can change the theme, 
view your profile and log out. On the dashboard itself, 5 buttons exist. You can:

1. List all existing users

2. List all existing exercises

3. Add an exercise

4. Add a user

5. Show all submitted solutions

## Add Exercise
At the moment only two exercise-types work:

1. Parsons-Puzzle
    
    - to create a Parsons-Puzzle click on `ADD EXERCISE` and `Parsons Puzzle`
    - you can provide a title, a description in Markdown format and different
    pieces (Python code will be syntax-highlighted)
    - be sure to provide the pieces in the right order as this will be the
    solution to your exercise
    - if you are done, click `SUBMIT NEW EXERCISE` and then `BACK TO OVERVIEW`
    - you now should see the exercise in the exercise list

2. Free Coding Exercise

    - to create a Free Coding Exercise click on `ADD EXERCISE` and `Free Coding Exercise`
    - you can provide a title, a description in Markdown, sample code, some
    test cases and the function name of the function that should be executed by
    our system
    - you can add several test cases with input parameters and expected output
    (at the moment only integers work as input and output)
    - if you are done click `SUBMIT NEW EXERCISE` and return to the base URL
    - you now should see the exercise in the exercise list

## Add User
The admin dashboard provides the functionality to add new user accounts. Just
fill in the register form.

## List Users
To list all existing accounts click on the `list all users` button.
Clicking on a user leads you to the profile page of this user.

## Solve an exercise
To solve exercises click on the exercise list, choose an exercise and click on
it. The symbol in the exercise list provides you the exercise type. Now you can
solve the chosen exercise. The solving time will be measured. If you click on
`SUBMIT` our system will automatically evaluate your solution. If you're done
click `BACK To OVERVIEW`. Your solution attempts are displayed at the solution
list.

## Show Solutions
To see a list of all solutions click on `SHOW ALL SOLUTIONS`.

## Log Out
To Log out click on your user-name on the top-right, then a dropdown menu opens.
There you can click on `Logout`.