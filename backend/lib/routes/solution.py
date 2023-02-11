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

import datetime
import json

from flask import Response, jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.core import config, utils
from backend.lib.evaluator.evaluator import eval_solution
from backend.lib.interfaces.database import SolutionModel, db_engine


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
            "solution_date", type=lambda x: datetime.datetime.fromtimestamp(x), help="{error_msg}", location="args"
        )
        parser.add_argument(
            "solution_duration", type=lambda x: datetime.timedelta(x), help="{error_msg}", location="args"
        )
        parser.add_argument("solution_correct", type=bool, help="{error_msg}", location="args")
        parser.add_argument("solution_pending", type=bool, help="{error_msg}", location="args")
        parser.add_argument("solution_content", type=dict, help="{error_msg}", location="args")
        parser.add_argument("solution_page", type=int, default=1, help="{error_msg}", location="args")
        parser.add_argument(
            "solution_limit",
            type=int,
            default=config.MAX_ITEMS_RETURNED,
            help="{error_msg}",
            location="args",
        )

        args = parser.parse_args()

        solutions = SolutionModel.query.order_by(SolutionModel.solution_id)
        if args["solution_id"]:
            solutions = solutions.where(SolutionModel.solution_id == args["solution_id"])
        if args["solution_user"]:
            solutions = solutions.where(SolutionModel.solution_user == args["solution_user"])
        if args["solution_exercise"]:
            solutions = solutions.where(SolutionModel.solution_exercise == args["solution_exercise"])
        if args["solution_date"]:
            lower = args["solution_date"].replace(hour=0, minute=0, second=0, microsecond=0)
            upper = lower + datetime.timedelta(days=1)
            solutions = solutions.where(sqlalchemy.between(SolutionModel.solution_date, lower, upper))
        if args["solution_duration"]:
            solutions = solutions.where(SolutionModel.solution_duration == args["solution_duration"])
        if args["solution_correct"]:
            solutions = solutions.where(SolutionModel.solution_correct == args["solution_correct"])
        if args["solution_pending"]:
            solutions = solutions.where(SolutionModel.solution_pending == args["solution_pending"])
        if args["solution_content"]:
            solutions = solutions.where(SolutionModel.solution_content == args["solution_content"])
        solutions = solutions.paginate(
            page=args["solution_page"], per_page=args["solution_limit"], max_per_page=config.MAX_ITEMS_RETURNED
        )

        response = dict(data=list(), meta=dict())
        for solution in solutions.items:
            # check for access for every resource, if client has no access for a certain resource the enpoint
            # immediately returns 401 or 403
            # _, auth, _ = utils.authorize(
            #     cookies=request.cookies, method="GET", endpoint="user", resourceId=solution.solution_id
            # )
            # if auth == None:
            #     return utils.makeResponseNewCookie(dict(message="Login required"), 401, request.cookies)
            # elif not auth:
            #     return utils.makeResponseNewCookie(dict(message="No Access"), 403, request.cookies)
            response["data"].append(solution.to_json())
        response["meta"]["total"] = solutions.total
        response["meta"]["next_page"] = solutions.next_num
        response["meta"]["prev_page"] = solutions.prev_num
        response["meta"]["next_url"] = (
            utils.get_url(request.url, solution_page=solutions.next_num) if solutions.has_next else None
        )
        response["meta"]["prev_url"] = (
            utils.get_url(request.url, solution_page=solutions.prev_num) if solutions.has_prev else None
        )
        response["meta"]["page_size"] = len(solutions.items)
        response["meta"]["pages"] = solutions.pages

        return make_response(jsonify(response), 200)
        # return utils.makeResponseNewCookie(response, 200, request.cookies)

    def post(self) -> Response:
        """
        Implementation of the HTTP POST method. Use this method to create a new solution. This method prevents
        duplication.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("solution_exercise", type=int, help="{error_msg}", required=True)
        parser.add_argument(
            "solution_date", type=lambda x: datetime.datetime.fromtimestamp(x), help="{error_msg}", required=True
        )
        parser.add_argument(
            "solution_duration", type=lambda x: datetime.timedelta(x), help="{error_msg}", required=True
        )
        parser.add_argument("solution_content", type=dict, help="{error_msg}", required=True)

        args = parser.parse_args()

        # check for access
        is_admin, auth, user_id = utils.authorize(cookies=request.cookies, method="POST", endpoint="solution")
        if auth == None:
            return utils.makeResponseNewCookie(dict(message="Login required"), 401, request.cookies)
        elif not auth:
            return utils.makeResponseNewCookie(dict(message="No Access"), 403, request.cookies)

        # evaluate solution attempt
        correct, pending = eval_solution(args["solution_content"], args["solution_exercise"])

        # load the solution table
        solution_table = sqlalchemy.Table(config.SOLUTION_TABLE, db_engine.metadata, autoload=True)
        # create a new element
        solution = SolutionModel(
            solution_user=user_id,
            solution_exercise=args["solution_exercise"],
            solution_date=args["solution_date"],
            solution_duration=args["solution_duration"],
            solution_correct=correct,
            solution_pending=pending,
            solution_content=json.dumps(args["solution_content"]),
        )
        # add the new element
        db_engine.session.add(solution)
        db_engine.session.commit()
        # check whether the element was added successfully
        subquery = (
            db_engine.select([sqlalchemy.func.max(solution_table.c.solution_id)])
            .select_from(solution_table)
            .scalar_subquery()
        )
        query = db_engine.select(["*"]).select_from(solution_table).where(solution_table.c.solution_id == subquery)
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        result = dict()
        row = selection.fetchone()
        result = dict(
            message="Successfully submitted solution",
            solution_id=row[0],
            solution_user=row[1],
            solution_exercise=row[2],
            solution_date=row[3],
            solution_duration=row[4],
            solution_correct=bool(row[5]),  # db reponds with 0 or 1 sometimes
            solution_pending=bool(row[6]),
            solution_content=json.loads(row[7]),
        )
        return utils.makeResponseNewCookie(result, 201, request.cookies)

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change a solution.

        Returns:
            Response: A HTTP response with the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("solution_id", type=int, help="{error_msg}", required=True)
        parser.add_argument("solution_exercise", type=int, help="{error_msg}")
        parser.add_argument("solution_date", type=lambda x: datetime.datetime.fromtimestamp(x), help="{error_msg}")
        parser.add_argument("solution_duration", type=lambda x: datetime.timedelta(x), help="{error_msg}")
        parser.add_argument("solution_correct", type=bool, help="{error_msg}")
        parser.add_argument("solution_pending", type=bool, help="{error_msg}")
        parser.add_argument("solution_content", type=dict, help="{error_msg}")

        args = parser.parse_args(strict=True)

        # check for access
        is_admin, auth, user_id = utils.authorize(
            cookies=request.cookies, method="PUT", endpoint="solution", resourceId=args["solution_id"]
        )
        if auth == None:
            return utils.makeResponseNewCookie(dict(message="Login required"), 401, request.cookies)
        elif not auth:
            return utils.makeResponseNewCookie(dict(message="No Access"), 403, request.cookies)

        solution = SolutionModel.query.filter_by(solution_id=args["solution_id"]).first_or_404(
            description=f"Solution with solution_id {args['solution_id']} does not exist"
        )

        if args["solution_exercise"]:
            solution.solution_exercise = args["solution_exercise"]
        if args["solution_date"]:
            solution.solution_date = args["solution_date"]
        if args["solution_duration"]:
            solution.solution_duration = args["solution_duration"]
        if args["solution_correct"]:
            solution.solution_correct = args["solution_correct"]

        db_engine.session.commit()

        result = dict(message=f"The solution with solution_id {args['solution_id']} was changed successfully")
        return utils.makeResponseNewCookie(result, 200, request.cookies)

    def delete(self) -> Response:
        """
        Implementation of the HTTP DELETE method. Use this method to delete a solution.

        Returns:
            Response: A HTTP response with the confirmation or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("solution_id", type=int, help="{error_msg}", required=True)

        args = parser.parse_args(strict=True)

        # check for access
        is_admin, auth, user_id = utils.authorize(
            cookies=request.cookies, method="POST", endpoint="exercise", resourceId=args["solution_id"]
        )
        if auth == None:
            return utils.makeResponseNewCookie(dict(message="Login required"), 401, request.cookies)
        elif not auth:
            return utils.makeResponseNewCookie(dict(message="No Access"), 403, request.cookies)

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
            return utils.makeResponseNewCookie(result, 404, request.cookies)

        result = dict(message=f"Successfully deleted solution with solution_id {args['solution_id']}")
        return utils.makeResponseNewCookie(result, 200, request.cookies)
