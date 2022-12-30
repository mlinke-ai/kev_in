#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Kev.in - a coding learning platform
# Copyright (C) 2022  Max Linke
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import Response, jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

import hashlib
import jwt

from backend.lib.interfaces.database import UserModel, db_engine
from backend.lib.core import config


class UserResource(Resource):
    def get(self) -> Response:
        """
        Implementation of the HTTP GET method. Use this method to query the system for users.
        If you pass user_id < 1, it will be ignored. If you pass multiple arguments, you query
        the system with multiple arguments. It is possible that the system returns up to
        config.MAX_ITEMS_RETURNED items. If your query would select more items, only the first
        20 items will be returned.
        

        Returns:
            Response: A HTTP response with all elements selected by the query in JSON or an error message.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        #in get requests the location of the data is in the arguments
        parser.add_argument("user_id", type=int, help="ID of the user is missing", location="args")
        parser.add_argument("user_name", type=str, help="Name of the user is missing", location="args")
        parser.add_argument("user_mail", type=str, help="Mail of the user is missing", location="args")
        parser.add_argument("user_admin", type=bool, help="Admin status is missing", location="args")
        parser.add_argument("user_sadmin", type=bool, help="SAdmin status is missing", location="args")

        args = parser.parse_args()

        #check if token cookie was sent
        cookies = request.cookies.to_dict(True) #we only use the first value from each key
        if not "token" in cookies:
            return make_response((jsonify(dict(message="Login required"))), 401)
        #check if the client has access
        if not self._authorize(cookies["token"], args["user_id"]):
            return make_response((jsonify(dict(message="No Access"))), 403)

        # load the user table
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # compose a query to select the requested element
        query = db_engine.select(user_table).select_from(user_table)
        if args["user_id"]:
            if args["user_id"] < 1: #primary key is somehow always > 0
                pass
            else:
                query = query.where(user_table.c.user_id == args["user_id"])
        if args["user_name"]:
            query = query.where(user_table.c.user_name == args["user_name"])
        if args["user_mail"]:
            query = query.where(user_table.c.user_mail == args["user_mail"])
        if args["user_admin"]:
            query = query.where(user_table.c.user_admin == args["user_admin"])
        if args["user_sadmin"]:
            query = query.where(user_table.c.user_id == args["user_sadmin"])
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        result = dict()
        for row in selection.fetchall():
            result[row[0]] = dict(user_id=row[0], user_name=row[1])
        
        if len(result) > config.MAX_ITEMS_RETURNED:
            result = dict(list(result.items())[0: config.MAX_ITEMS_RETURNED])
        
        return make_response((jsonify(result)), 200)

    def post(self) -> Response:
        """
        Implementation of the HTTP POST method. Use this method to create a new user. This method prevents duplication.
        Here no Authorization is needed, except for creating an admin account.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, help="Name of the user is missing", required=True)
        parser.add_argument("user_pass", type=str, help="Credentials of the user are missing", required=True)
        parser.add_argument("user_mail", type=str, help="Mail of the user is missing", required=True)
        parser.add_argument("user_admin", type=bool, help="Admin status is missing", required=True)

        args = parser.parse_args()

        if args["user_admin"]: #somebody wants to create an admin account
            #check if token cookie was sent
            cookies = request.cookies.to_dict(True) #we only use the first value from each key
            if not "token" in cookies:
                return make_response((jsonify(dict(message="Login required"))), 401)
            #check if the client has access
            if not self._authorize(cookies["token"], change_admin=True):
                return make_response((jsonify(dict(message="No Access"))), 403)

        # load the user table
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # compose the query
        query = (
            db_engine.select([sqlalchemy.func.count()])
            .select_from(user_table)
            .where(user_table.c.user_name == args["user_name"])
        )
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # check wether the selection contains an element
        if selection.scalar() == 0:
            # if the selection contains no elements it means we can safely create the new element
            # create a new element
            user = UserModel(
                user_name=args["user_name"],
                user_pass=hashlib.sha256(bytes(args["user_pass"], encoding="utf-8")).hexdigest(),
                user_mail=args["user_mail"],
                user_admin=args["user_admin"],
                user_sadmin=False
                )
            # add the new element
            db_engine.session.add(user)
            db_engine.session.commit()
            # compose a query to check wether the new element was added successfully
            # TODO: query for last created element not based on given parameters
            query = (
                db_engine.select([user_table.c.user_name, user_table.c.user_id])
                .select_from(user_table)
                .where(user_table.c.user_name == args["user_name"])
            )
            # execute the query and store the result
            selection = db_engine.session.execute(query)
            try:
                # get the only element from the selection
                row = selection.fetchone()
            except sqlalchemy.exc.NoResultFound:
                # if there is no element the element could not be added
                result = dict(message="An error occurred while creating the user")
                return make_response((jsonify(result)), 500)
            else:
                result = dict(message="The user was created successfully", user_name=row.user_name, user_id=row.user_id)
                return make_response((jsonify(result)), 201)
        else:
            # if the selection contains an element we can't create a new one as would create a duplicate
            result = dict(message="A user with this name already exists")
            return make_response((jsonify(result)), 409)
        # return the new element (importend for the ID) or an error message

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change a user.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, help="ID of the user is missing", required=True)
        parser.add_argument("user_name", type=str, help="Name of the user is missing")
        parser.add_argument("user_pass", type=str, help="Credentials of the user are missing")
        parser.add_argument("user_mail", type=str, help="Mail of the user is missing")
        parser.add_argument("user_admin", type=bool, help="Admin status is missing")

        args = parser.parse_args()

        #check if token cookie was sent
        cookies = request.cookies.to_dict(True) #we only use the first value from each key
        if not "token" in cookies:
            return make_response((jsonify(dict(message="Login required"))), 401)
        #check if the client has access
        if not self._authorize(cookies["token"], args["user_id"], args["user_admin"]):
            return make_response((jsonify(dict(message="No Access"))), 403)

        # load the user table
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # drop the ID as we don't want to update it
        values = args.copy()
        del values["user_id"]
        # compose the query to update the requested element
        query = db_engine.update(user_table).where(user_table.c.user_id == args["user_id"]).values(values)
        # execute the query
        selection = db_engine.session.execute(query)
        db_engine.session.commit()

        #if no element was updated, the rowcount is 0
        if selection.rowcount == 0:
            result = dict(message=f"User with user_id {args['user_id']} does not exist")
            return make_response((jsonify(result)), 404)

        result = dict(message=f"Successfully chanaged user with user_id {args['user_id']}")
        return make_response((jsonify(result)), 200)

    def delete(self) -> dict:
        """
        Implementation of the HTTP DELETE method. Use this method to delete a user.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, help="ID of the user is missing", required=True)

        args = parser.parse_args()

        #check if token cookie was sent
        cookies = request.cookies.to_dict(True) #we only use the first value from each key
        if not "token" in cookies:
            return make_response((jsonify(dict(message="Login required"))), 401)
        #check if the client has access
        if not self._authorize(cookies["token"], args["user_id"]):
            return make_response((jsonify(dict(message="No Access"))), 403)

        # load the user table
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # compose the query to delete the requested element
        query = db_engine.delete(user_table).where(user_table.c.user_id == args["user_id"])
        # execute the query
        selection = db_engine.session.execute(query)
        db_engine.session.commit()
        
        #if no element was updated, the rowcount is 0
        if selection.rowcount == 0:
            result = dict(message=f"User with user_id {args['user_id']} does not exist")
            return make_response((jsonify(result)), 404)

        result = dict(message=f"Successfully deleted user with user_id {args['user_id']}")
        return make_response((jsonify(result)), 200)

    def _authorize(self, token: str, user_id: int = None, change_admin: bool = False) -> bool:
        """
        This method is used to determine if a certain client has the right to change or access data, based on the
        HTTP request. Therefore the JWT is decoded. Returns True if access is granted and False when access is denied.
        This method grants access to all admins and to users, if they want to access or change their own data.

        Params:
            `token`:    the JWT, the client sends with it's request
            `user_id`:  the user_id of the user acocunt about which the client wants to access or change data
            `change_admin`: True, if the client wants to change the admin status of an account to True or wants to
                            create an admin account

        Returns:
            `True` if access is granted, otherwise `False`
        """
        
        #decode JWT to dict
        try:
            user_data = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            return False
 
        #now check in database if the user exists
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        query = db_engine.select(user_table).select_from(user_table).where(user_table.c.user_id == user_data["user_id"])
        selection = db_engine.session.execute(query)
        try:
            row = selection.fetchone()
        except sqlalchemy.exc.NoResultFound:
            return False
        else:
            if row["user_admin"]: #our client is an admin
                return True
            elif user_id == None: #in POST when somebody wants to create an admin account but is no admin
                return False 
            else: #our client is no admin and wants to access/change data from a certain account
                #if client can access/change data from own account, but can't change admin status
                return (user_id == row["user_id"]) and (not change_admin) 