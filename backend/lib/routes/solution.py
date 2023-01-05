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

from backend.lib.interfaces.database import SolutionModel, db_engine
from backend.lib.core import config


class SolutionResource(Resource):
    def get(self) -> Response:
        """
        Implementation of the HTTP GET method. Use this method to query the system for solutions.
        If you pass user_id < 1 or exercise_id < 1, it will be ignored. If you pass multiple arguments, your query
        the system with multiple arguments. The system returns only up to config.MAX_ITEMS_RETURNED items.

        Returns:
            Response: A HTTP response with all elements selected by the query in JSON or an error message.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        # define arguments
        parser.add_argument("solution_id", type=int, help="ID of the solution is missing", location="args")
        parser.add_argument("solution_user", type=int, help="ID of the user is missing", location="args")
        parser.add_argument("solution_exercise", type=int, help="ID of the exercise is missing", location="args")
        # TODO: lookup correct type
        parser.add_argument("solution_date", type=int, help="Start time of the solution is missing", location="args")
        # TODO: lookup correct type
        parser.add_argument("solution_duration", type=int, help="Duration of the solution is missing", location="args")
        parser.add_argument("solution_correct", type=bool, help="Correctness of solution is missing", location="args")
        parser.add_argument("solution_offset", type=int, default=0, help="Start index is missing")
        parser.add_argument("solution_limit", type=int, default=config.MAX_ITEMS_RETURNED, help="Page size is missing")

        args = parser.parse_args()

        # check if page limit is in range
        if args["solution_limit"] not in range(config.MAX_ITEMS_RETURNED + 1):
            return make_response(
                jsonify(dict(message="Page limit no tin range", min_limit=0, max_limit=config.MAX_ITEMS_RETURNED)), 400
            )

        # check if token cookie was sent
        cookies = request.cookies.to_dict(True)  # we only use the first value from each key
        if not "token" in cookies:
            return make_response(jsonify(dict(message="Login required")), 401)
        # check if the client has access
        if not self._authorize(cookies["token"], args["user_id"]):
            return make_response(jsonify(dict(message="No access")), 403)

        # load the solution table
        solution_table = sqlalchemy.Table(config.SOLUTION_TABLE, db_engine.metadata, autoload=True)
        # compose a query to select the requested element
        query = db_engine.select(solution_table).select_from(solution_table)
        if args["solution_id"]:
            query = query.where(solution_table.c.solution_id == args["solution_id"])
        else:
            query = query.where(solution_table.c.solution_id >= args["solution_offset"])
            query = query.limit(args["solution_limit"])
        if args["solution_user"]:
            query = query.where(solution_table.c.solution_user == args["solution_user"])
        if args["solution_exercise"]:
            query = query.where(solution_table.c.solution_exercise == args["solution_exercise"])
        if args["solution_date"]:
            query = query.where(solution_table.c.solution_date == args["solution_date"])
        if args["solution_duration"]:
            query = query.where(solution_table.c.solution_duration == args["solution_duration"])
        if args["solution_correct"]:
            query = query.where(solution_table.c.solution_correct == args["solution_correct"])
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        result = dict()
        for row in selection.fetchall():
            result[row[0]] = dict(
                solution_id=row[0],
                solution_user=row[1],
                solution_exercise=row[2],
                solution_date=row[3],
                solution_duration=row[4],
                solution_correct=row[5],
            )

        return make_response(jsonify(result), 200)

    def post(self) -> Response:
        """
        Implementation of the HTTP POST method. Use this method to create a new solution. This method prevents duplication.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("solution_user", type=int, help="ID of the user is missing", required=True, location="args")
        parser.add_argument(
            "solution_exercise", type=int, help="ID of the exercise is missing", required=True, location="args"
        )
        parser.add_argument(
            "solution_date", type=int, help="Date of the solution is missing", required=True, location="args"
        )
        parser.add_argument(
            "solution_duration", type=int, help="Duration of the solution is missing", required=True, location="args"
        )

        args = parser.parse_args()

        # check if token cookie was sent
        cookies = request.cookies.to_dict(True)  # we only use the first value from each key
        if not "token" in cookies:
            return make_response(jsonify(dict(message="Login required")), 401)
        # check if the client has access
        if not self._authorize(cookies["token"], args["user_id"]):
            return make_response(jsonify(dict(message="No access")), 403)

        # TODO: evaluate solution attempt (the evaluator should return whether the attempt was correct or not)
        correct = True

        # load the solution table
        solution_table = sqlalchemy.Table(config.SOLUTION_TABLE, db_engine.metadata, autoload=True)
        # create a new element
        solution = SolutionModel(
            solution_user=args["solution_user"],
            solution_exercise=args["solution_Exercise"],
            solution_date=args["solution_args"],
            solution_duration=args["solution_duration"],
            solution_correct=correct,
        )
        # add the new element
        db_engine.session.add(solution)
        db_engine.session.commit()
        # check whether the element was added successfully
        query = db_engine.select([sqlalchemy.func.max(solution_table.c.solution_id)]).select_from(solution_table)
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        result = dict()
        row = selection.fetchone()
        result = dict(
            solution_id=row[0],
            solution_user=row[1],
            solution_exercise=row[2],
            solution_date=row[3],
            solution_duration=row[4],
            solution_correct=row[5],
        )
        return make_response(jsonify(result), 200)

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change a solution.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("solution_id", type=int, help="ID of the solution is missing", required=True)
        parser.add_argument("solution_user", type=int, help="ID of the user is missing")
        parser.add_argument("solution_exercise", type=int, help="ID of the exercise is missing")
        # TODO: lookup correct type
        parser.add_argument("solution_date", type=int, help="Start time of the solution is missing")
        # TODO: lookup correct type
        parser.add_argument("solution_duration", type=int, help="Duration of the solution is missing")
        parser.add_argument("solution_correct", type=bool, help="Correctness of solution is missing")

        args = parser.parse_args()

        # check if the token cookie was sent
        # TODO: this should be admins only
        cookies = request.cookie.to_dict(True)  # we only use the value from each key
        if not "token" in cookies:
            return make_response(jsonify(dict(message="Login required")), 401)
        # check if the client has access
        if not self._authorized(cookies["token"]):
            return make_response(jsonify(dict(message="No Access")), 403)

        # load the solution table
        solution_table = sqlalchemy.Table(config.SOLUTION_TABLE, db_engine.metadata, autoload=True)
        # drop the ID as we don#t want to update it
        values = args.copy()
        del values["solution_id"]
        # compose the query to update the requested element
        query = (
            db_engine.update(solution_table).where(solution_table.c.solution_id == args["solution_id"]).values(values)
        )
        # execute the query
        selection = db_engine.session.execute(query)
        db_engine.session.commit()

        # if no element was updated, the rowcount is 0

        if selection.rowcount == 0:
            result = dict(message=f"Solution with solution_id {args['solution_id']} does not exist")
            return make_response(jsonify(result), 404)

        result = dict(message=f"The solution with solution_id {args['solution_id']} was changed successfully")
        return make_response(jsonify(result), 200)

    def delete(self) -> Response:
        """
        Implementation of the HTTP DELETE method. Use this method to delete a solution.

        Returns:
            Response: A HTTP response with the confirmation or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("solution_id", type=int, help="ID of the solution is missing", required=True)

        args = parser.parse_args()

        # check if token cookie was sent
        # TODO: this should be admins only
        cookies = request.cookies.to_dict(True)  # we only use the first value from each key
        if not "token" in cookies:
            return make_response(jsonify(dict(message="Login required")), 401)
        # check if the client has access
        if not self._authorize(cookies["token"], args["solution_id"]):
            return make_response(jsonify(dict(message="No access")), 403)

        # load the solution table
        solution_table = sqlalchemy.Table(config.SOLUTION_TABLE, db_engine.metadata, autoload=True)
        # compose the query to delete the requested element
        query = db_engine.delete(solution_table).where(solution_table.c.solution_id == args["solution_id"])
        # execute the query
        selection = db_engine.session.execute(query)
        db_engine.session.commit()

        # if no element was updated, the rowcount is 0
        if selection.rowcount == 0:
            result = dict(message=f"Solution with solution_id {args['solution_id']} does not exist")
            return make_response(jsonify(result), 404)

        result = dict(message=f"Successfully deleted solution with solution_id {args['solution_id']}")
        return make_response(jsonify(result), 200)

    def _authorize(self, toke: str, solution_id: int = None, change_admin: bool = False) -> bool:
        """
        This method is used to determine if a certain client has the right to change or access data, based on the
        HTTP request. Therefore the JWT is decoded. Returns True if access is granted and False when access is denied.
        TODO: grand access only for admins

        Args:
            toke (str): The JWT token the client sends with the request.
            solution_id (int, optional): The ID of the solution which the client wants to access. Defaults to None.
            change_admin (bool, optional): True, if the client wants to change the admin status of a user or wants to create an admins account. TODO: do we need this flag?. Defaults to False.

        Returns:
            bool: True, if access is granted, otherwise False.
        """

        # TODO: rewrite the function as utility
        return True
