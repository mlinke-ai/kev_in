#!/usr/bin/python3
# -*- coding: utf-8 -*-
import jwt

from werkzeug.datastructures import ImmutableMultiDict
from typing import Any
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.core.config import JWT_SECRET, UserRole, USER_TABLE, SOLUTION_TABLE
from backend.lib.interfaces.database import db_engine

def authorize(cookies: ImmutableMultiDict, method: str, endpoint: str, resourceId: int = None, changeToAdmin: bool = None) -> tuple[bool, bool | None]:
    """
    The authorize funciton which determines, if a user has rights to access certain data or not.

    Args: 
        cookies: :class:`ImmutableMultiDict`
            All cookies, the client sents with his request. You can pass `request.cookies`.
        method: :class:`str`
            The HTTP method this function should authenticate. Should be one of the following: 
            (GET, POST, PUT, DELETE)
        endpoint: :class:`str`
            The HTTP method this function should authenticate. Should be one of the following: 
            (exercise, user, solution)
        reqResourceId: :class:`int`
            The id of the resource, the client requested, only needed when `method=='GET', 'PUT' or 'DELETE'`,
            exept for the exercise endpoint.
        changeToAdmin: :class:`bool`
            Only needs to be set, on user PUT mehtod.
    Returns:
        A tuple of Type :class:`tuple[bool, bool | None]` (is_admin, has_access)
        is_admin can be True or False (Depending on wether the client is an admin or not)
        has_access can be True, False or None (None if no valid JWT was sent)
    """
    
    if method not in ['GET', 'POST', 'PUT', 'DELETE']:
        raise ValueError("Argument 'method' should contain one of the following: 'GET', 'POST', 'PUT', 'DELETE'")

    if endpoint not in ['exercise', 'user', 'solution']:
        raise ValueError("Argument 'endpoint' should contain one of the following: 'exercise', 'user', 'solution'")

    if method in ['GET','PUT', 'DELETE'] and resourceId == None and endpoint != 'exercise':
        raise ValueError(f"'method' is {method}, 'endpoint' is {endpoint} and no 'recourceId' was provided")

    if method == 'PUT' and endpoint == 'user' and changeToAdmin == False:
        raise ValueError(f"'method' is {method}, 'endpoint' is {endpoint} and no 'changeToAdmin' was provided")

    user_data = _extractUserData(cookies)

    if user_data == None:
        return False, None

    role = _getUserRole(user_data["user_id"])

    if role == None:
        return False, None #non existing user tries to access data

    if endpoint == 'exercise':
        return not(role == UserRole.User) ,_authExercise(role, method)
    elif endpoint == 'user':
        return not(role == UserRole.User) ,_authUser(role, method, int(user_data["user_id"]), resourceId, changeToAdmin)
    elif endpoint == 'solution':
        return not(role == UserRole.User) ,_authSolution(role, method, int(user_data["user_id"]), resourceId)

def getUseridFromCookies(cookies: ImmutableMultiDict) -> int | None:
    """
    Get the user_id argument from cookies. Returns None if no valid JWT
    is in the cookies.
    """

    user_data = _extractUserData(cookies)

    if user_data == None:
        return None

    return user_data["user_id"]
    
        
def _extractUserData(cookies: ImmutableMultiDict) -> dict[str, Any] | None:
    """
    Extracts the user data from cookies. The user data is everything, what is stored in the JWT.
    Therefor see `backend/lib/routes/login.py`
    """
    
    try:
        token = cookies.getlist("token")
    except KeyError:
        return None #no value for key 'token' exists

    if len(token) != 1: 
        return None #more than one value for key 'token' exists

    try:
        user_data = jwt.decode(token[0], JWT_SECRET, algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        return None #token could not be extracted
    else:
        return user_data

def _getUserRole(user_id: int) -> UserRole | None:
    """
    Checks what role a user has, given the user_id.
    """

    user_table = sqlalchemy.Table(USER_TABLE, db_engine.metadata, autoload=True)
    query = db_engine.select(user_table).select_from(user_table).where(user_table.c.user_id == user_id)
    selection = db_engine.session.execute(query)
    try:
        row = selection.fetchone()
        role = UserRole(row["user_role"])
    except (sqlalchemy.exc.NoResultFound, TypeError):
        return None #the user with the given id was not found in the database

    return role

def _authExercise(role: UserRole, method: str) -> bool:
    """
    Access determiation for exercise endpoint.
    """

    if method == "GET":
        return True
    elif method == "POST":
        return not (role == UserRole.User)
    elif method == "PUT":
        return not (role == UserRole.User)
    elif method == "DELETE":
        return not (role == UserRole.User)

def _authUser(role: UserRole, method: str, userId: int, resourceId: int, changeToAdmin: bool) -> bool:
    """
    Access determiation for user endpoint.
    """

    if method == "GET" or method == "DELETE":
        if role == UserRole.User:
            #check if client want's to access its own data
            user_table = sqlalchemy.Table(USER_TABLE, db_engine.metadata, autoload=True)
            query = db_engine.select(user_table).select_from(user_table).where(user_table.c.user_id == resourceId)
            selection = db_engine.session.execute(query)
            try:
                row = selection.fetchone()
            except sqlalchemy.exc.NoResultFound:
                return False #we're sure here that client don't want to access its own data
            return userId == row["user_id"]
        else:
            return True

    elif method == "POST":
        return True #this is never reached because user POST does not need authorization

    elif method == "PUT":
        if role == UserRole.User and changeToAdmin:
            return False
        elif role == UserRole.User:
            #check if client want's to access its own data
            user_table = sqlalchemy.Table(USER_TABLE, db_engine.metadata, autoload=True)
            query = db_engine.select(user_table).select_from(user_table).where(user_table.c.user_id == resourceId)
            selection = db_engine.session.execute(query)
            try:
                row = selection.fetchone()
            except sqlalchemy.exc.NoResultFound:
                return False #we're sure here that client don't want to access its own data
            return userId == row["user_id"]
        else:
            return True

def _authSolution(role: UserRole, method: str, userId: int, resourceId: int) -> bool:
    """
    Access determiation for solution endpoint.
    """

    if method == "GET" or method == "PUT" or method == "DELETE":
        if role == UserRole.User:
            #check if client want's to access its own data
            solution_table = sqlalchemy.Table(SOLUTION_TABLE, db_engine.metadata, autoload=True)
            query = db_engine.select(solution_table).select_from(solution_table).where(solution_table.c.user_id == resourceId)
            selection = db_engine.session.execute(query)
            try:
                row = selection.fetchone()
            except sqlalchemy.exc.NoResultFound:
                return False #we're sure here that client don't want to access its own data
            return userId == row["user_relation"]
    elif method == "POST":
        return True