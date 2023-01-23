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

from backend.lib.interfaces.database import UserModel, db_engine
from backend.lib.core import config, utils


class UserResource(Resource):
    def get(self) -> Response:
        """
        Implementation of the HTTP GET method. Use this method to query the system for users.

        Returns:
            Response: A HTTP response with all elements selected by the query in JSON or an error message.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, default=0, help="{error_msg}", location="args")
        parser.add_argument("user_name", type=str, default="", help="{error_msg}", location="args")
        parser.add_argument("user_mail", type=str, default="", help="{error_msg}", location="args")
        parser.add_argument(
            "user_role",
            type=lambda x: config.UserRole(int(x)),
            default=config.UserRole.User,
            help="{error_msg}",
            location="args"
        )
        parser.add_argument("user_offset", type=int, default=0, help="{error_msg}", location="args")
        parser.add_argument("user_limit", type=int, default=config.MAX_ITEMS_RETURNED, help="{error_msg}", location="args")

        args = parser.parse_args()

        # check if page limit is in range
        if args["user_limit"] not in range(config.MAX_ITEMS_RETURNED + 1):
            return make_response(
                jsonify(dict(message="Page limit not in range", min_limit=0, max_limit=config.MAX_ITEMS_RETURNED)), 400
            )

        # load the user table
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # compose a query to select the requested element
        query = db_engine.select(user_table).select_from(user_table)

        if len(request.url.split("?")) == 1: #a request with no arguments was sent
            #return the user data from the logged in user
            id = utils.getUseridFromCookies(request.cookies)
            if id == None:
                return make_response((jsonify(dict(message="Login required"))), 401)
            query = query.where(user_table.c.user_id == id)
            selection = db_engine.session.execute(query)
            row = selection.fetchone()

            result = dict()
            result[int(row["user_id"])] = dict(
                user_id=int(row["user_id"]),
                user_name=str(row["user_name"]),
                user_mail=str(row["user_mail"]),
                user_role=row["user_role"].name
            )
            response = make_response(jsonify(result), 200)
            utils.attachNewCookie(response, request.cookies)
            return response
            
        if args["user_id"]:
            query = query.where(user_table.c.user_id == args["user_id"])
        else:
            query = query.where(user_table.c.user_id >= args["user_offset"])
            query = query.limit(args["user_limit"])
        if args["user_name"]:
            query = query.where(user_table.c.user_name == args["user_name"])
        if args["user_mail"]:
            query = query.where(user_table.c.user_mail == args["user_mail"])
        if args["user_role"]:
            query = query.where(user_table.c.user_role == args["user_role"])
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        result = dict()
        for row in selection.fetchall():

            #check for access for every resource, if client has no access for a certain resource the enpoint immediately returns 401 or 403
            is_admin, auth = utils.authorize(
                cookies= request.cookies,
                method= "GET",
                endpoint= "user",
                resourceId= int(row["user_id"])
            )
            if auth == None:
                return make_response((jsonify(dict(message="Login required"))), 401)
            elif not auth:
                return make_response((jsonify(dict(message="No Access"))), 403)

            result[int(row["user_id"])] = dict(
                user_id=int(row["user_id"]),
                user_name=str(row["user_name"]),
                user_mail=str(row["user_mail"]),
                user_role=row["user_role"].name,
            )

        response = make_response(jsonify(result), 200)
        utils.attachNewCookie(response, request.cookies)
        return response

    def post(self) -> Response:
        """
        Implementation of the HTTP POST method. Use this method to create a new user. This method prevents duplication.
        Here no Authorization is needed, except for creating an admin account.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, help="{error_msg}", required=True)
        parser.add_argument("user_pass", type=str, help="{error_msg}", required=True)
        parser.add_argument("user_mail", type=str, help="{error_msg}", required=True)

        args = parser.parse_args()

        if args["user_name"] == "":
            return make_response(jsonify(dict(message="user_name must not be empty")), 400)
        if args["user_pass"] == "":
            return make_response(jsonify(dict(message="user_pass must not be empty")), 400)
        if args["user_mail"] == "":
            return make_response(jsonify(dict(message="user_mail must not be empty")), 400)

        # create a new element
        user = UserModel(
            user_name=args["user_name"],
            user_pass=hashlib.sha256(bytes(args["user_pass"], encoding="utf-8")).hexdigest(),
            user_mail=args["user_mail"],
            user_role=config.UserRole.User,
        )
        db_engine.session.add(user)
        try:
            db_engine.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # TODO: should we do a rollback at this point?
            # db_engine.session.rollback()
            return make_response(jsonify(dict(message="A user with this mail already exists")), 409)
        else:
            response = make_response(
                jsonify(
                    dict(
                        message="The user was created successfully",
                        user_id=user.user_id,
                        user_name=user.user_name,
                        user_mail=user.user_mail,
                        user_role=user.user_role,
                    )
                ),
                201,
            )
            utils.attachNewCookie(response, request.cookies)
            return response

        # TODO: the method above is way more elegant; we should remove the lower part
        # # load the user table
        # user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # # compose the query
        # query = (
        #     db_engine.select([sqlalchemy.func.count()])
        #     .select_from(user_table)
        #     .where(user_table.c.user_name == args["user_name"])
        # )
        # # execute the query and store the selection
        # selection = db_engine.session.execute(query)
        # # check wether the selection contains an element
        # if selection.scalar() == 0:
        #     # if the selection contains no elements it means we can safely create the new element
        #     # create a new element
        #     user = UserModel(
        #         user_name=args["user_name"],
        #         user_pass=hashlib.sha256(bytes(args["user_pass"], encoding="utf-8")).hexdigest(),
        #         user_mail=args["user_mail"],
        #         user_role=args["user_role"],
        #     )
        #     # add the new element
        #     db_engine.session.add(user)
        #     db_engine.session.commit()
        #     # compose a query to check wether the new element was added successfully
        #     query = (
        #         db_engine.select(user_table).select_from(user_table).where(user_table.c.user_name == args["user_name"])
        #     )
        #     # execute the query and store the result
        #     selection = db_engine.session.execute(query)
        #     try:
        #         # get the only element from the selection
        #         row = selection.fetchone()
        #     except sqlalchemy.exc.NoResultFound:
        #         # if there is no element the element could not be added
        #         result = dict(message="An error occurred while creating the user")
        #         return make_response((jsonify(result)), 500)
        #     else:
        #         result = dict(
        #             message="The user was created successfully", user_id=row[0], user_name=row[1], user_mail=row[3]
        #         )
        #         return make_response((jsonify(result)), 201)
        # else:
        #     # if the selection contains an element we can't create a new one as it would create a duplicate
        #     result = dict(message="A user with this name already exists")
        #     return make_response((jsonify(result)), 409)

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change a user.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, help="{error_msg}", required=True)
        parser.add_argument("user_name", type=str, help="{error_msg}")
        parser.add_argument("user_pass", type=str, help="{error_msg}")
        parser.add_argument("user_mail", type=str, help="{error_msg}")
        parser.add_argument("user_role", type=lambda x: config.UserRole(int(x)), help="{error_msg}")

        args = parser.parse_args()

        if args["user_name"] == "":
            return make_response(jsonify(dict(message="user_name must not be empty")), 400)
        if args["user_pass"] == "":
            return make_response(jsonify(dict(message="user_pass must not be empty")), 400)
        if args["user_mail"] == "":
            return make_response(jsonify(dict(message="user_mail must not be empty")), 400)

        if args["user_role"] == config.UserRole.SAdmin: #prevent creating super admin
            return make_response((jsonify(dict(message="No Access"))), 403)

        #check for access
        is_admin, auth = utils.authorize(
            cookies= request.cookies,
            method= "PUT",
            endpoint= "user",
            resourceId= args["user_id"],
            changeToAdmin=(not args["user_role"]==config.UserRole.User)
            )
        if auth == None:
            return make_response((jsonify(dict(message="Login required"))), 401)
        elif not auth:
            return make_response((jsonify(dict(message="No Access"))), 403)

        user = UserModel.query.filter_by(user_id=args["user_id"]).first_or_404()
        if args["user_name"]:
            user.user_name = args["user_name"]
        if args["user_mail"]:
            user.user_mail = args["user_mail"]
        if args["user_pass"]:
            user.user_pass = args["user_pass"]
        try:
            db_engine.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # TODO: should we do a rollback at this point?
            # db_engine.session.rollback()
            return make_response(jsonify(dict(message="A user with this mail already exists")), 409)
        else:
            response = make_response(jsonify(dict(message="Changed properties successfully")), 200)
            utils.attachNewCookie(response, request.cookies)
            return response

        # TODO: the method above is way more elegant; we should remove the lower part
        # # load the user table
        # user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # # drop the ID as we don't want to update it
        # values = args.copy()
        # del values["user_id"]
        # # compose the query to update the requested element
        # query = db_engine.update(user_table).where(user_table.c.user_id == args["user_id"]).values(values)
        # # execute the query
        # selection = db_engine.session.execute(query)
        # db_engine.session.commit()

        # # if no element was updated, the rowcount is 0
        # if selection.rowcount == 0:
        #     result = dict(message=f"User with user_id {args['user_id']} does not exist")
        #     return make_response((jsonify(result)), 404)

        # result = dict(message=f"Successfully changed user with user_id {args['user_id']}")
        # return make_response((jsonify(result)), 200)

    def delete(self) -> dict:
        """
        Implementation of the HTTP DELETE method. Use this method to delete an user.

        Returns:
            Response: A HTTP response with the confirmation or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, help="{error_msg}", required=True)

        args = parser.parse_args()

        #check for access
        is_admin, auth = utils.authorize(
            cookies= request.cookies,
            method= "DELETE",
            endpoint= "user",
            resourceId= args["user_id"]
            )
        if auth == None:
            return make_response((jsonify(dict(message="Login required"))), 401)
        elif not auth:
            return make_response((jsonify(dict(message="No Access"))), 403)

        # load the user table
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # compose the query to delete the requested element
        query = db_engine.delete(user_table).where(user_table.c.user_id == args["user_id"])
        # execute the query
        selection = db_engine.session.execute(query)
        db_engine.session.commit()

        # if no element was updated, the rowcount is 0
        if selection.rowcount == 0:
            result = dict(message=f"User with user_id {args['user_id']} does not exist")
            return make_response((jsonify(result)), 404)

        result = dict(message=f"Successfully deleted user with user_id {args['user_id']}")
        response = make_response(jsonify(result), 200)
        utils.attachNewCookie(response, request.cookies)
        return response
