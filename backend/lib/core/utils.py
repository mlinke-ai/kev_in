#!/usr/bin/python3
# -*- coding: utf-8 -*-
import jwt

from werkzeug.datastructures import ImmutableMultiDict
from typing import Any
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.core.config import JWT_SECRET, UserRole, USER_TABLE, SOLUTION_TABLE
from backend.lib.interfaces.database import db_engine

def authorize(cookies: ImmutableMultiDict, method: str, endpoint: str, resourceId: int = None) -> bool | None:
    """
    The authorize funciton which determines, if a user has rights to access certain data or not.

    Args: 
        cookies: :class:`ImmutableMultiDict`
            All cookies, the client sents with his request. You can pass `request.cookies`.
        method: :class:`str`
            The HTTP method this function should authenticate. Should be one of the following: 
            (GET, POST, PUT, DELETE)
        endpoint: :class:`str`
            The HTTP method this function shoul authenticate. Should be one of the following: 
            (exercise, user, solution)
        reqResourceId: :class:`int`
            The id of the resource, the client requested, only needed when `method=='GET' or 'PUT'`,
            exept for the exercise endpoint.
    Returns:
        `True` if access is granted,
        `False`if access is denied,
        `None` if no valid JWT were in the cookies
    """
    
    if method not in ['GET', 'POST', 'PUT', 'DELETE']:
        raise ValueError("Argument 'method' should contain one of the following: 'GET', 'POST', 'PUT', 'DELETE'")

    if endpoint not in ['exercise', 'user', 'solution']:
        raise ValueError("Argument 'endpoint' should contain one of the following: 'exercise', 'user', 'solution'")

    if method in ['GET','PUT'] and resourceId == None and endpoint != 'exercise':
        raise ValueError(f"'method' is {method} and no 'recourceId' was provided")

    user_data = _extractUserData(cookies)

    if user_data == None:
        return None

    role = _getUserRole(user_data["user_id"])

    if role == None:
        raise ValueError("The given user has no role.")

    if endpoint == 'exercise':
        return _authExercise(role, method)
    elif endpoint == 'user':
        return _authUser(role, method, int(user_data["user_id"]), resourceId)
    elif endpoint == 'solution':
        return _authSolution(role, method, int(user_data["user_id"]), resourceId)
    
        

def _extractUserData(cookies: ImmutableMultiDict) -> dict[str, Any] | None:
    """
    Extracts the user data from cookies.
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
    except sqlalchemy.exc.NoResultFound:
        return None #the user with the given id was not found in the database

    return UserRole(row["user_role"])

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

def _authUser(role: UserRole, method: str, userId: int, recourceId: str) -> bool:
    """
    Access determiation for user endpoint.
    """

    if method == "GET" or method == "PUT":
        if role == UserRole.User:
            #check if client want's to access its own data
            user_table = sqlalchemy.Table(USER_TABLE, db_engine.metadata, autoload=True)
            query = db_engine.select(user_table).select_from(user_table).where(user_table.c.user_id == recourceId)
            selection = db_engine.session.execute(query)
            try:
                row = selection.fetchone()
            except sqlalchemy.exc.NoResultFound:
                return False #we're sure here that client don't want to access its own data
            return userId == row["user_id"]
        else:
            return True
    elif method == "POST":
        return True
    elif method == "DELETE":
        return not (role == UserRole.User)

def _authSolution(role: UserRole, method: str, userId: int, recourceId: int) -> bool:
    """
    Access determiation for solution endpoint.
    """

    if method == "GET" or method == "PUT":
        if role == UserRole.User:
            #check if client want's to access its own data
            solution_table = sqlalchemy.Table(SOLUTION_TABLE, db_engine.metadata, autoload=True)
            query = db_engine.select(solution_table).select_from(solution_table).where(solution_table.c.user_id == recourceId)
            selection = db_engine.session.execute(query)
            try:
                row = selection.fetchone()
            except sqlalchemy.exc.NoResultFound:
                return False #we're sure here that client don't want to access its own data
            return userId == row["user_relation"]
    elif method == "POST":
        return True
    elif method == "DELETE":
        return not (role == UserRole.User)