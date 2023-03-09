#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Kev.in - a coding learning platform
# Copyright (C) 2022 to 2023  Max Linke and others
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

from flask import Response, current_app, jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, set_access_cookies, verify_jwt_in_request
from flask_restful import Resource, inputs, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.database.models import ExerciseLanguage, ExerciseModel, ExerciseType, UserRole, db
from backend.utils import get_url


class ExerciseResource(Resource):
    def __init__(self) -> None:
        # create a parser for the GET request data
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("exercise_id", type=int, help="{error_msg}", action="append", location="args")
        self.get_parser.add_argument("exercise_title", type=str, help="{error_msg}", location="args")
        self.get_parser.add_argument("exercise_description", type=str, help="{error_msg}", location="args")
        self.get_parser.add_argument(
            "exercise_type", type=lambda x: ExerciseType(int(x)), help="{error_msg}", location="args"
        )
        self.get_parser.add_argument("exercise_content", type=dict, help="{error_msg}", location="args")
        self.get_parser.add_argument("exercise_solution", type=dict, help="{error_msg}", location="args")
        self.get_parser.add_argument(
            "exercise_language", type=lambda x: ExerciseLanguage(int(x)), help="{error_msg}", location="args"
        )
        self.get_parser.add_argument("exercise_page", type=int, default=0, help="{error_msg}", location="args")
        self.get_parser.add_argument(
            "exercise_limit",
            type=int,
            default=current_app.config["MAX_ITEMS_RETURNED"],
            help="{error_msg}",
            location="args",
        )
        self.get_parser.add_argument(
            "exercise_details", type=inputs.boolean, default=False, help="{error_msg}", location="args"
        )
        # create a parser for the POST request data
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument("exercise_title", type=str, help="{error_msg}", required=True)
        self.post_parser.add_argument("exercise_description", type=str, help="{error_msg}", required=True)
        self.post_parser.add_argument("exercise_content", type=dict, help="{error_msg}", required=True)
        self.post_parser.add_argument("exercise_solution", type=dict, help="{error_msg}", required=True)
        self.post_parser.add_argument(
            "exercise_type", type=lambda x: ExerciseType(int(x)), help="{error_msg}", required=True
        )
        self.post_parser.add_argument(
            "exercise_language", type=lambda x: ExerciseLanguage(int(x)), help="{error_msg}", required=True
        )
        # create a parser for the PUT request data
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument("exercise_id", type=int, help="{error_msg}", required=True)
        self.put_parser.add_argument("exercise_title", type=str, help="{error_msg}")
        self.put_parser.add_argument("exercise_description", type=str, help="{error_msg}")
        self.put_parser.add_argument("exercise_content", type=dict, help="{error_msg}")
        self.put_parser.add_argument("exercise_solution", type=dict, help="{error_msg}")
        self.put_parser.add_argument("exercise_type", type=lambda x: ExerciseType(int(x)), help="{error_msg}")
        self.put_parser.add_argument("exercise_language", type=lambda x: ExerciseLanguage(int(x)), help="{error_msg}")
        # create a parser for the DELETE request data
        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument("exercise_id", type=int, help="{error_msg}", required=True)

    def get(self) -> Response:
        """
        Implementation of the HTTP GET method. Use this method to query the system for exercises.

        Returns:
            Response: A HTTP response with all elements selected by the query in JSON or an error message.
        """
        token = verify_jwt_in_request()

        args = self.get_parser.parse_args()

        query = db.select(ExerciseModel).order_by(ExerciseModel.exercise_id)
        if args["exercise_id"] is not None:
            query = query.filter(ExerciseModel.exercise_id.in_(args["exercise_id"]))
        if args["exercise_title"] is not None:
            query = query.where(ExerciseModel.exercise_title == args["exercise_title"])
        if args["exercise_description"] is not None:
            query = query.where(ExerciseModel.exercise_description == args["exercise_description"])
        if args["exercise_type"] is not None:
            query = query.where(ExerciseModel.exercise_type == args["exercise_type"])
        if args["exercise_content"] is not None:
            query = query.where(ExerciseModel.exercise_content == args["exercise_content"])
        if args["exercise_solution"] is not None:
            query = query.where(ExerciseModel.exercise_solution == args["exercise_solution"])
        if args["exercise_language"] is not None:
            query = query.where(ExerciseModel.exercise_language == args["exercise_language"])
        exercises = db.paginate(
            query,
            page=args["exercise_page"],
            per_page=args["exercise_limit"],
            max_per_page=current_app.config["MAX_ITEMS_RETURNED"],
        )

        if exercises.total == 0:
            return make_response(jsonify(dict()), 204)

        response = dict(data=list(), meta=dict())
        for exercise in exercises.items:
            response["data"].append(
                exercise.to_json(args["exercise_details"], get_jwt_identity()["user_role_value"] != 3)
            )
        response["meta"]["total"] = exercises.total
        response["meta"]["next_page"] = exercises.next_num
        response["meta"]["prev_page"] = exercises.prev_num
        response["meta"]["next_url"] = (
            get_url(request.url, user_page=exercises.next_num) if exercises.has_next else None
        )
        response["meta"]["prev_url"] = (
            get_url(request.url, user_page=exercises.prev_num) if exercises.has_prev else None
        )
        response["meta"]["page_size"] = len(exercises.items)
        response["meta"]["pages"] = exercises.pages

        return make_response(jsonify(response), 200)

    def post(self) -> Response:
        """
        Implementation of the HTTP POST method. Use this method to create a new exercise.
        This method ensures uniqueness of the exercise.

        Returns:
            Response: A HTTP response with the newly created exercise.
        """
        token = verify_jwt_in_request()

        args = self.post_parser.parse_args(strict=True)

        if args["exercise_title"] == "":
            return make_response(jsonify(dict(message="exercise_title must not be empty")), 400)
        if args["exercise_content"] == "":
            return make_response(jsonify(dict(message="exercise_content must not be empty")), 400)
        if args["exercise_solution"] == "":
            return make_response(jsonify(dict(message="exercise_solution must no be empty")), 400)

        exercise = ExerciseModel(
            args["exercise_title"],
            args["exercise_description"],
            args["exercise_type"],
            args["exercise_content"],
            args["exercise_solution"],
            args["exercise_language"],
        )
        db.session.add(exercise)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return make_response(dict(message="An exercise with this title does already exist"), 409)
        else:
            token = create_access_token(identity=exercise.to_json())
            response = make_response(jsonify(exercise.to_json()), 201)
            set_access_cookies(response, token)
            return response

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change exercise attributes.
        This method ensures uniqueness of the exercise.

        Returns:
            Response: A HTTP response with the new exercise attributes.
        """
        token = verify_jwt_in_request()

        args = self.put_parser.parse_args(strict=True)

        if args["exercise_title"] == "":
            return make_response(jsonify(dict(message="exercise_title must not be empty")), 400)
        if args["exercise_content"] == "":
            return make_response(jsonify(dict(message="exercise_content must not be empty")), 400)
        if args["exercise_solution"] == "":
            return make_response(jsonify(dict(message="exercise_solution must not be empty")), 400)

        query = db.select(ExerciseModel).filter_by(exercise_id=args["exercise_id"])
        exercise = db.one_or_404(query, description="An exercise with this ID does not exist.")
        if args["exercise_title"] is not None:
            exercise.exercise_title = args["exercise_title"]
        if args["exercise_description"] is not None:
            exercise.exercise_description = args["exercise_description"]
        if args["exercise_type"] is not None:
            exercise.exercise_type = args["exercise_type"]
        if args["exercise_content"] is not None:
            exercise.exercise_content = args["exercise_content"]
        if args["exercise_solution"] is not None:
            exercise.exercise_solution = args["exercise_solution"]
        if args["exercise_language"] is not None:
            exercise.exercise_language = args["exercise_language"]
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return make_response(jsonify(dict(message="An error occurred while updating the exercise")), 409)
        else:
            return make_response(jsonify(dict(message="Changed properties successfully")), 200)

    def delete(self) -> Response:
        """
        Implementation of the HTTP DELETE method. Use this method to delete an exercise.

        Returns:
            Response: A HTTP response with a success message.
        """
        token = verify_jwt_in_request()

        args = self.delete_parser.parse_args(strict=True)

        if get_jwt_identity()["user_role_value"] != UserRole.User.value:
            query = db.select(ExerciseModel).filter_by(exercise_id=args["exercise_id"])
            exercise = db.one_or_404(query, description="An exercise with this ID does not exist.")
            db.session.delete(exercise)
            db.session.commit()
            response = make_response(jsonify(dict(message="Exercise deleted successfully")), 200)
        else:
            response = make_response(jsonify(dict(message="Users are not authorized to perform this action.")), 403)
        return response
