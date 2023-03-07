#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from flask import Response, current_app, jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, set_access_cookies, verify_jwt_in_request
from flask_restful import Resource, inputs, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.database.models import SolutionModel, UserRole, db
from backend.utils import get_url, user_id_from_token


class SolutionResource(Resource):
    def __init__(self) -> None:
        # create a parser for the GET request data
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("solution_id", type=int, help="{error_msg}", location="args")
        self.get_parser.add_argument("solution_user", type=int, help="{error_msg}", location="args")
        self.get_parser.add_argument("solution_exercise", type=int, help="{error_msg}", location="args")
        self.get_parser.add_argument(
            "solution_date", type=lambda x: datetime.datetime.fromtimestamp(int(x)), help="{error_msg}", location="args"
        )
        self.get_parser.add_argument(
            "solution_duration", type=lambda x: datetime.timedelta(seconds=int(x)), help="{error_msg}", location="args"
        )
        self.get_parser.add_argument("solution_correct", type=inputs.boolean, help="{error_msg}", location="args")
        self.get_parser.add_argument("solution_pending", type=inputs.boolean, help="{error_msg}", location="args")
        self.get_parser.add_argument("solution_content", type=dict, help="{error_msg}", location="args")
        self.get_parser.add_argument("solution_page", type=int, default=1, help="{error_msg}", location="args")
        self.get_parser.add_argument(
            "solution_limit",
            type=int,
            default=current_app.config["MAX_ITEMS_RETURNED"],
            help="{error_msg}",
            location="args",
        )
        # create a parser for the POST request data
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument("solution_user", type=int, help="{error_msg}", required=True)
        self.post_parser.add_argument("solution_exercise", type=int, help="{error_msg}", required=True)
        self.post_parser.add_argument(
            "solution_date", type=lambda x: datetime.datetime.fromtimestamp(int(x)), help="{error_msg}", required=True
        )
        self.post_parser.add_argument(
            "solution_duration", type=lambda x: datetime.timedelta(seconds=int(x)), help="{error_msg}", required=True
        )
        self.post_parser.add_argument("solution_content", type=dict, help="{error_msg}", required=True)
        # create a parser for the PUT request data
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument("solution_id", type=int, help="{error_msg}", required=True)
        self.put_parser.add_argument("solution_user", type=int, help="{error_msg}")
        self.put_parser.add_argument("solution_exercise", type=int, help="{error_msg}")
        self.put_parser.add_argument(
            "solution_date", type=lambda x: datetime.datetime.fromtimestamp(int(x)), help="{error_msg}"
        )
        self.put_parser.add_argument(
            "solution_duration", type=lambda x: datetime.timedelta(seconds=int(x)), help="{error_msg}"
        )
        self.put_parser.add_argument("solution_correct", type=inputs.boolean, help="{error_msg}")
        self.put_parser.add_argument("solution_pending", type=inputs.boolean, help="{error_msg}")
        self.put_parser.add_argument("solution_content", type=dict, help="{error_msg}")
        # create a parser for the DELETE request data
        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument("solution_id", type=int, help="{error_msg}", required=True)

    def get(self) -> Response:
        """
        Implementation of the HTTP GET method. Use this method to query the system for solutions.

        Returns:
            Response: A HTTP response with all elements selected by the query in JSON or an error message.
        """
        token = verify_jwt_in_request()

        args = self.get_parser.parse_args()

        query = db.select(SolutionModel).order_by(SolutionModel.solution_id)
        if args["solution_id"] is not None:
            query = query.filter(SolutionModel.solution_id.in_(args["solution_id"]))
        if args["solution_user"] is not None:
            query = query.where(SolutionModel.solution_user == args["solution_user"])
        if args["solution_exercise"] is not None:
            query = query.where(SolutionModel.solution_exercise == args["solution_exercise"])
        if args["solution_date"] is not None:
            lower = args["solution_date"].replace(hour=0, minute=0, second=0, microsecond=0)
            upper = lower + datetime.timedelta(days=1)
            query = query.where(sqlalchemy.between(SolutionModel.solution_date, lower, upper))
        if args["solution_duration"] is not None:
            query = query.where(SolutionModel.solution_duration == args["solution_duration"])
        if args["solution_correct"] is not None:
            query = query.where(SolutionModel.solution_correct == args["solution_Correct"])
        if args["solution_pending"] is not None:
            query = query.where(SolutionModel.solution_pending == args["solution_pending"])
        if args["solution_content"] is not None:
            query = query.where(SolutionModel.solution_content == args["solution_content"])
        solutions = db.paginate(
            query,
            page=args["solution_page"],
            per_page=args["solution_limit"],
            max_per_page=current_app.config["MAX_ITEMS_RETURNED"],
        )

        if solutions.total == 0:
            return make_response(jsonify(dict()), 204)

        response = dict(data=list(), meta=dict())
        for solution in solutions.items:
            response["data"].append(solution.to_json())
        response["meta"]["total"] = solutions.total
        response["meta"]["next_page"] = solutions.next_num
        response["meta"]["prev_page"] = solutions.prev_num
        response["meta"]["next_url"] = (
            get_url(request.url, user_page=solutions.next_num) if solutions.has_next else None
        )
        response["meta"]["prev_url"] = (
            get_url(request.url, user_page=solutions.prev_num) if solutions.has_prev else None
        )
        response["meta"]["page_size"] = len(solutions.items)
        response["meta"]["pages"] = solutions.pages

        return make_response(jsonify(response), 200)

    def post(self) -> Response:
        """
        Implementation of the HTTP POST method. Use this method to create a solution.

        Returns:
            Response: A HTTP response with the newly created solution.
        """
        token = verify_jwt_in_request()

        args = self.post_parser.parse_args(strict=True)

        if args["solution_content"] == "":
            return make_response(jsonify(dict(message="solution_content must not be empty")), 400)

        correct, pending = True, False

        solution = SolutionModel(
            args["solution_user"],
            args["solution_exercise"],
            args["solution_date"],
            args["solution_duration"],
            correct,
            pending,
            args["solution_content"],
        )
        db.session.add(solution)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return make_response(dict(message="An user with this mail does already exist"), 409)
        else:
            token = create_access_token(identity=solution.to_json())
            response = make_response(jsonify(solution.to_json()), 201)
            set_access_cookies(response, token)
            return response

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change solution attributes.

        Returns:
            Response: A HTTP response with the new solution attributes.
        """
        token = verify_jwt_in_request()

        args = self.put_parser.parse_args(strict=True)

        if args["solution_content"] == "":
            return make_response(jsonify(dict(message="solution_content must not be empty")), 400)

        query = db.select(SolutionModel).filter_by(solution_id=args["solution_id"])
        solution = db.one_or_404(query, description="A solution with this ID does not exist.")
        if args["solution_user"] is not None:
            solution.solution_user = args["solution_user"]
        if args["solution_exercise"] is not None:
            solution.solution_exercise = args["solution_exercise"]
        if args["solution_date"] is not None:
            solution.solution_date = args["solution_date"]
        if args["solution_duration"] is not None:
            solution.solution_duration = args["solution_duration"]
        if args["solution_correct"] is not None:
            solution.solution_correct = args["solution_correct"]
        if args["solution_pending"] is not None:
            solution.solution_pending = args["solution_pending"]
        if args["solution_content"] is not None:
            solution.solution_content = args["solution_content"]
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return make_response(jsonify(dict(message="An error occurred while updating the solution")), 409)
        else:
            return make_response(jsonify(dict(message="Changed properties successfully")), 200)

    def delete(self) -> Response:
        """
        Implementation of the HTTP DELETE method. Use this method to delete a solution.

        Returns:
            Response: A HTTP response with a success message.
        """
        token = verify_jwt_in_request()

        args = self.delete_parser.parse_args(strict=True)

        if get_jwt_identity()["user_role_value"] != UserRole.User.value:
            query = db.select(SolutionModel).filter_by(user_id=args["user_id"])
            solution = db.one_or_404(query, description="A solution with this ID does not exist.")
            db.session.delete(solution)
            db.session.commit()
            response = make_response(jsonify(dict(message="Solution deleted successfully")), 200)
        else:
            response = make_response(jsonify(dict(message="Users are not authorized to perform this action.")), 403)
        return response
