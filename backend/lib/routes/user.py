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

from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.interfaces.database import UserModel, db_engine


class UserResource(Resource):
    def get(self) -> dict:
        """Implementation of the HTTP GET method. Use this method to query the system for users.
        TODO: add explanation o fall request fields.

        Returns:
            dict: All elements selected by the query in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, help="ID of the user is missing")
        parser.add_argument("user_name", type=str, help="Name of the user is missing")
        # TODO: add more user properties
        args = parser.parse_args()
        # load the user table
        user_table = sqlalchemy.Table("user_model", db_engine.metadata, autoload=True)
        # compose a query to select the requested element
        query = db_engine.select(user_table).select_from(user_table)
        if args["user_id"]:
            query = query.where(user_table.c.user_id == args["user_id"])
        if args["user_name"]:
            query = query.where(user_table.c.user_name == args["user_name"])
        result = dict()
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        for row in selection.fetchall():
            result[row[0]] = dict(user_id=row[0], user_name=row[1])
        return result

    def post(self) -> dict:
        """Implementation of the HTTP POST method. Use this method to create a new user. This method prevents duplication.
        TODO: add explanation of all request fields

        Returns:
            dict: Either the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, help="Name of the user is missing", required=True)
        parser.add_argument("user_pass", type=str, help="Credentials of the user are missing", required=True)
        # TODO: add more user properties
        args = parser.parse_args()
        # load the user table
        user_table = sqlalchemy.Table("user_model", db_engine.metadata, autoload=True)
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
            user = UserModel(user_name=args["user_name"], user_pass=args["user_pass"])
            # add the new element
            db_engine.session.add(user)
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
                row = selection.scalar_one()
            except sqlalchemy.exc.NoResultFound:
                # if there is no element the element could not be added
                result = dict(message="An error occurred while creating the user")
            else:
                # if the element got added commit the changes
                db_engine.session.commit()
                result = dict(message="The user was created successfully", user_name=row.user_name, user_id=row.user_id)
        else:
            # if the selection contains an element we can't create a new one as would create a duplicate
            result = dict(message="A user with this name already exists")
        # return the new element (importend for the ID) or an error message
        return result

    def put(self) -> dict:
        """Implementation of the HTTP PUT method. Use this method to change a user.
        TODO: add explanation of all request fields

        Returns:
            dict: TODO: add return message
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, help="ID of the user is missing")
        parser.add_argument("user_name", type=str, help="Name of the user is missing")
        # TODO: add more user properties
        args = parser.parse_args()
        # load the user table
        user_table = sqlalchemy.Table("user_model", db_engine.metadata, autoload=True)
        # drop the ID as we don't want to update it
        values = args.copy()
        del values["user_id"]
        # compose the query to update the requested element
        query = db_engine.update(user_table).where(user_table.c.user_id == args["user_id"]).values(values)
        result = dict()
        # execute the query (the selection is not needed)
        selection = db_engine.session.execute(query)
        db_engine.session.commit()
        return result

    def delete(self) -> dict:
        """Implementation of the HTTP DELETE method. Use this method to delete a user.
        TODO: add explanation of all request fields

        Returns:
            dict: TODO: add return message
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, help="ID of the user is missing", required=True)
        # TODO: do we really need any other argument besides the ID?
        parser.add_argument("user_name", type=str, help="Name of the user is missing")
        args = parser.parse_args()
        # load the user table
        user_table = sqlalchemy.Table("user_model", db_engine.metadata, autoload=True)
        # compose the query to delete the requested element
        query = db_engine.delete(user_table).where(user_table.c.user_id == args["user_id"])
        if args["user_name"]:
            query = query.where(user_table.c.user_name == args["user_name"])
        result = dict()
        # execute the query (the selection is not needed)
        selection = db_engine.session.execute(query)
        db_engine.session.commit()
        return result
