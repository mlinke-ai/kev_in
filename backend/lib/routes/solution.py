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

from backend.lib.interfaces.database import SolutionModel, db_engine
from backend.lib.core import config, utils

import datetime


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
        parser.add_argument("solution_id", type=int, help="{error_msg}", location="args")
        parser.add_argument("solution_user", type=int, help="{error_msg}", location="args")
        parser.add_argument("solution_exercise", type=int, help="{error_msg}", location="args")
        parser.add_argument(
            "solution_date",
            type=lambda x: datetime.datetime.fromtimestamp(x),
            help="{error_msg}",
            location="args"
            )
        parser.add_argument(
            "solution_duration",
            type=lambda x: datetime.timedelta(x),
            help="{error_msg}",
            location="args"
            )
        parser.add_argument("solution_correct", type=bool, help="{error_msg}", location="args")
        parser.add_argument("solution_offset", type=int, default=0, help="{error_msg}", location="args")
        parser.add_argument(
            "solution_limit", type=int, default=config.MAX_ITEMS_RETURNED, help="{error_msg}", location="args"
        )

        args = parser.parse_args()

        # check if page limit is in range
        if args["solution_limit"] not in range(config.MAX_ITEMS_RETURNED + 1):
            return make_response(
                jsonify(dict(message="Page limit no tin range", min_limit=0, max_limit=config.MAX_ITEMS_RETURNED)), 400
            )

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

            # check for access for every resource, if client has no access for a certain resource the enpoint immediately returns 401 or 403
            is_admin, auth = utils.authorize(
                cookies=request.cookies, method="GET", endpoint="user", resourceId=int(row[0])
            )
            if auth == None:
                return make_response((jsonify(dict(message="Login required"))), 401)
            elif not auth:
                return make_response((jsonify(dict(message="No Access"))), 403)

            result[row[0]] = dict(
                solution_id=row[0],
                solution_user=row[1],
                solution_exercise=row[2],
                solution_date=str(row[3]),
                solution_duration=str(row[4]),
                solution_correct=row[5],
            )

        response = make_response(jsonify(result), 200)
        utils.attachNewCookie(response, request.cookies)
        return response

    def post(self) -> Response:
        """
        Implementation of the HTTP POST method. Use this method to create a new solution. This method prevents duplication.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("solution_exercise", type=int, help="{error_msg}", required=True)
        parser.add_argument(
            "solution_date",
            type=lambda x: datetime.datetime.fromtimestamp(x),
            help="{error_msg}",
            required=True
        )
        parser.add_argument("solution_duration",
            type=lambda x: datetime.timedelta(x),
            help="{error_msg}",
            required=True
        )

        args = parser.parse_args()

        # check for access
        is_admin, auth = utils.authorize(
            cookies= request.cookies,
            method= "POST",
            endpoint= "solution"
            )
        if auth == None:
            return make_response((jsonify(dict(message="Login required"))), 401)
        elif not auth:
            return make_response((jsonify(dict(message="No Access"))), 403)

        # TODO: evaluate solution attempt (the evaluator should return whether the attempt was correct or not)
        correct = True

        # load the solution table
        solution_table = sqlalchemy.Table(config.SOLUTION_TABLE, db_engine.metadata, autoload=True)
        # create a new element
        solution = SolutionModel(
            solution_user=utils.getUseridFromCookies(request.cookies),
            solution_exercise=args["solution_exercise"],
            solution_date=args["solution_date"],
            solution_duration=args["solution_duration"],
            solution_correct=correct
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
            solution_user=solution.solution_user,
            solution_exercise=solution.solution_exercise,
            solution_date=str(solution.solution_date),
            solution_duration=str(solution.solution_duration),
            solution_correct=solution.solution_correct
        )
        response = make_response(jsonify(result), 201)
        utils.attachNewCookie(response, request.cookies)
        return response

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change a solution.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("solution_id", type=int, help="{error_msg}", required=True)
        parser.add_argument("solution_user", type=int, help="{error_msg}")
        parser.add_argument("solution_exercise", type=int, help="{error_msg}")
        parser.add_argument(
            "solution_date",
            type=lambda x: datetime.datetime.fromtimestamp(x),
            help="{error_msg}"
        )
        parser.add_argument("solution_duration",
            type=lambda x: datetime.timedelta(x),
            help="{error_msg}"
        )
        parser.add_argument("solution_correct", type=bool, help="{error_msg}")

        args = parser.parse_args()

        # check for access
        is_admin, auth = utils.authorize(
            cookies=request.cookies, method="PUT", endpoint="solution", resourceId=args["solution_id"]
        )
        if auth == None:
            return make_response((jsonify(dict(message="Login required"))), 401)
        elif not auth:
            return make_response((jsonify(dict(message="No Access"))), 403)

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
        response = make_response(jsonify(result), 200)
        utils.attachNewCookie(response, request.cookies)
        return response

    def delete(self) -> Response:
        """
        Implementation of the HTTP DELETE method. Use this method to delete a solution.

        Returns:
            Response: A HTTP response with the confirmation or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("solution_id", type=int, help="{error_msg}", required=True)

        args = parser.parse_args()

        # check for access
        is_admin, auth = utils.authorize(
            cookies=request.cookies, method="POST", endpoint="exercise", resourceId=args["solution_id"]
        )
        if auth == None:
            return make_response((jsonify(dict(message="Login required"))), 401)
        elif not auth:
            return make_response((jsonify(dict(message="No Access"))), 403)

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
        response = make_response(jsonify(result), 200)
        utils.attachNewCookie(response, request.cookies)
        return response
