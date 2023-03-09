---
title: Kev.in
summary: A learning platform form programming beginners.
authors:
    - Max Linke
    - and others
date: 2022-11-26
---

# Administrator manual

## Log-In
If you on the starting page click on the `START NOW` button to log in an
existing account or to create a new one. By default the Database provides two
accounts tuser and sadmin (credentials of sadmin can be found in the documentation in
api/config). Since our Log in system works with cookies, you're able to stay
logged in even if you close your browser (the cookie disappears after one hour).

## Admin Dashboard
If you successfully logged in, you should see the admin dashboard. On the first
time visiting this page you may get an error because no exercises exist by
default. On the top right you can see the you username. By clicking on that a
dropdown menu opens where you can change the theme and log out. On the
dashboard itself, 5 buttons exist. You can:

1. List all existing users

2. List all existing exercises

3. Add an exercise

4. Add a user

5. Show all your submitted solutions

## Add Exercise
At the moment only two Exercise-Types work:

1. Parsons-Puzzle
    
    - To create a Parsons-Puzzle click on `ADD EXERCISE` and `Parsons Puzzle`
    - you can provide a Title, a description in Markdown format and different
    pieces (Python code will be syntax-highlighted)
    - be sure to provide the pieces in the right order as this will be the
    solution to your exercise
    - if you are done click `SUBMIT NEW EXERCISE` and then `BACK TO OVERVIEW`
    - you now should see the exercise in the exercise list

2. Free Coding Exercise

    - To create a Parsons-Puzzle click on `ADD EXERCISE` and `Free Coding Exercise`
    - you can provide a Title, a description in Markdown, sample code, some
    test cases and the function name of the function that should be executed by
    our system
    - you can add several test cases with input parameters and expected output
    (at the moment only strings work input and output)
    - if you are done click `SUBMIT NEW EXERCISE` and return to the base URL
    - you now should see the exercise in the exercise list

## Add User
The admin dashboard provides the functionality to add new user accounts. Just
fill in the register form.

## List Users
To list all accounts click on the `list all users` button.

## Solve an exercise
To solve exercises click on the exercise list, chose an exercise and click on
it. The symbol in the exercise list provides you the exercise type. Now you can
solve the chosen exercise. The solving time will be measured. If you click on
`SUBMIT` our system wil automatically evaluate your solution. If you're done
click `BACK To OVERVIEW`. Your solution attempts can be seen at the solution
list.

## Show Solutions
To see a list of all your solutions click on `SHOW ALL SOLUTIONS`.

## Log Out
To Log out click on your user-name on the top-right, then a dropdown menu opens.
There you can click on `Logout`.