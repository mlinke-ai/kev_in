#!/usr/bin/python3
# -*- coding: utf-8 -*-
import jwt

from werkzeug.datastructures import ImmutableMultiDict
from typing import Any
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.core.config import JWT_SECRET, UserRole, USER_TABLE
from backend.lib.interfaces.database import db_engine

def authorize(cookies: ImmutableMultiDict, method: str, **kwargs) -> bool | None:
    """
    The authorize funciton which determines, if a user has rights to access certain data or not.

    Args: 
        cookies: :class:`ImmutableMultiDict`
            All cookies, the client sents with his request. You can pass `request.cookies`.
        
    """
    
    user_data = extractUserData(cookies)

    if user_data == None:
        return None

    role = getUserRole(user_data["user_id"])

    if role == None:
        return None


def extractUserData(cookies: ImmutableMultiDict) -> dict[str, Any] | None:
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

def getUserRole(user_id: str) -> UserRole | None:
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