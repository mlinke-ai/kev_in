#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Response, request
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.core import config, utils
from backend.lib.interfaces.database import ExerciseModel, db_engine


class ExerciseResource(Resource):
    def get(self) -> Response:
        """
        Implementation of the HTTP GET method. Use this method to query the system for exercises.
        You can get exercises by their id. If you pass exercise_id < 1, it will be ignored.
        If you pass multiple arguments, you query the system with multiple arguments. It is possible
        that the system returns up to config.MAX_ITEMS_RETURNED items. If your query would select
        more items, only the first 20 items will be returned

        Returns:
            Response: A HTTP response with all selected items in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="{error_msg}", location="args")
        parser.add_argument("exercise_title", type=str, help="{error_msg}", location="args")
        parser.add_argument("exercise_description", type=str, help="{error_msg}", location="args")
        parser.add_argument(
            "exercise_type",
            type=lambda x: config.ExerciseType(int(x)),
            help="{error_msg}",
            location="args",
        )
        parser.add_argument("exercise_content", type=dict, help="{error_msg}", location="args")
        parser.add_argument("exercise_solution", type=dict, help="{error_msg}", location="args")
        parser.add_argument(
            "exercise_language",
            type=lambda x: config.ExerciseLanguage(int(x)),
            help="{error_msg}",
            location="args",
        )
        parser.add_argument("exercise_offset", type=int, default=0, help="{error_msg}", location="args")
        parser.add_argument(
            "exercise_limit",
            type=int,
            default=config.MAX_ITEMS_RETURNED,
            help="{error_msg}",
            location="args",
        )
        parser.add_argument(
            "exercise_details",
            type=bool,
            default=False,
            help="{error_msg}",
            location="args",
        )

        args = parser.parse_args()

        # check if page limit is in range
        if args["exercise_limit"] not in range(config.MAX_ITEMS_RETURNED + 1):
            return utils.makeResponseNewCookie(
                dict(message="Page limit not in range", min_limit=0, max_limit=config.MAX_ITEMS_RETURNED),
                400,
                request.cookies,
            )

        # check for access
        is_admin, auth, user_id = utils.authorize(cookies=request.cookies, method="GET", endpoint="exercise")
        if auth == None:
            return utils.makeResponseNewCookie(dict(message="Login required"), 401, request.cookies)
        elif not auth:
            return utils.makeResponseNewCookie(dict(message="No Access"), 403, request.cookies)

        # load the exercise table
        exercise_table = sqlalchemy.Table(config.EXERCISE_TABLE, db_engine.metadata, autoload=True)
        # compose a query to select the requested element
        query = db_engine.select(exercise_table).select_from(exercise_table)
        if args["exercise_id"]:
            query = query.where(exercise_table.c.exercise_id == args["exercise_id"])
        else:
            query = query.where(exercise_table.c.exercise_id >= args["exercise_offset"])
            query = query.limit(args["exercise_limit"])
        if args["exercise_title"]:
            query = query.where(exercise_table.c.exercise_title == args["exercise_title"])
        if args["exercise_description"]:
            query = query.where(exercise_table.c.exercise_description == args["exercise_description"])
        if args["exercise_type"]:
            query = query.where(exercise_table.c.exercise_type == args["exercise_type"])
        if args["exercise_content"]:
            query = query.where(exercise_table.c.exercise_content == args["exercise_content"])
        if args["exercise_solution"]:
            query = query.where(exercise_table.c.exercise_solution == args["exercise_content"])
        if args["exercise_language"]:
            query = query.where(exercise_table.c.exercise_language == args["exercise_language"])
        result = dict()
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        # for row in selection.fetchall():
        #     print(row)
        #     if args["exercise_details"]:
        #         result[int(row["exercise_id"])] = dict(
        #             exercise_id=int(row["exercise_id"]),
        #             exercise_title=str(row["exercise_title"]),
        #             exercise_description=str(row["exercise_description"]),
        #             exercise_type=row["exercise_type"].name,
        #             exercise_content=str(row["exercise_content"]),
        #             exercise_solution=str(row["exercise_solution"]),
        #             exercise_language=row["exercise_language"].name,
        #         )
        #     else:
        #         result[int(row["exercise_id"])] = dict(
        #             exercise_id=int(row["exercise_id"]),
        #             exercise_title=str(row["exercise_title"]),
        #             exercise_type=row["exercise_type"].name,
        #             exercise_language=row["exercise_language"].name,
        #         )
        for row in selection.fetchall():
            if args["exercise_details"]:
                result[int(row[0])] = dict(
                    exercise_id=int(row[0]),
                    exercise_title=str(row[1]),
                    exercise_description=str(row[2]),
                    exercise_type=row[3].name,
                    exercise_content=utils.prepareExerciseContent(json.loads(row[4]), row[3].value),
                    exercise_solution=json.loads(row[5]),
                    exercise_language=row[6].name,
                )
            else:
                result[int(row[0])] = dict(
                    exercise_id=int(row[0]),
                    exercise_title=str(row[1]),
                    exercise_type=row[3].name,
                    exercise_language=row[6].name,
                )

        return utils.makeResponseNewCookie(result, 200, request.cookies)

    def post(self) -> Response:
        """
        Implementation of the HTTP POST method. Use this method to create a new exercise. This method prevents duplications.

        Returns:
            Response: Either the new element or an error message in JSON as HTTP response.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_title", type=str, help="{error_msg}", required=True)
        parser.add_argument("exercise_description", type=str, help="{error_msg}", required=True)
        parser.add_argument(
            "exercise_type",
            type=lambda x: config.ExerciseType(int(x)),
            help="{error_msg}",
            required=True,
        )
        parser.add_argument("exercise_content", type=dict, help="{error_msg}", required=True)
        parser.add_argument("exercise_solution", type=dict, help="{error_msg}", required=True)
        parser.add_argument(
            "exercise_language", type=lambda x: config.ExerciseLanguage(int(x)), help="{error_msg}", required=True
        )

        args = parser.parse_args()

        # check for access
        is_admin, auth, user_id = utils.authorize(cookies=request.cookies, method="POST", endpoint="exercise")
        if auth == None:
            return utils.makeResponseNewCookie(dict(message="Login required"), 401, request.cookies)
        elif not auth:
            return utils.makeResponseNewCookie(dict(message="No Access"), 403, request.cookies)

        # create a new element
        exercise = ExerciseModel(
            exercise_title=args["exercise_title"],
            exercise_description=args["exercise_description"],
            exercise_type=args["exercise_type"],
            exercise_content=json.dumps(args["exercise_content"]),
            exercise_solution=json.dumps(args["exercise_solution"]),
            exercise_language=args["exercise_language"],
        )
        db_engine.session.add(exercise)
        try:
            db_engine.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # TODO: should we do a rollback at this point?
            # db_engine.session.rollback()
            return utils.makeResponseNewCookie(
                dict(message="An exercise with this title already exists"), 409, request.cookies
                )
        else:
            return utils.makeResponseNewCookie(
                dict(
                    message="The exercise was created successfully",
                    exercise_id=exercise.exercise_id,
                    exercise_title=exercise.exercise_title,
                    exercise_description=exercise.exercise_description,
                    exercise_content=json.loads(exercise.exercise_content),
                ),
                201,
                request.cookies
            )

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change an exercise.
        All given Attributes will be changed. (except for exercise_id)

        Returns:
            Response: Either a success message, or an error message as HTTP response.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="{error_msg}", required=True)
        parser.add_argument("exercise_title", type=str, help="{error_msg}")
        parser.add_argument("exercise_description", type=str, help="{error_msg}")
        parser.add_argument(
            "exercise_type",
            type=lambda x: config.ExerciseType(int(x)),
            help="{error_msg}",
        )

        args = parser.parse_args()

        # check for access
        is_admin, auth, user_id = utils.authorize(cookies=request.cookies, method="PUT", endpoint="exercise")
        if auth == None:
            return utils.makeResponseNewCookie(dict(message="Login required"), 401, request.cookies)
        elif not auth:
            return utils.makeResponseNewCookie(dict(message="No Access"), 403, request.cookies)

        exercise = ExerciseModel.query.filter_by(exercise_id=args["exercise_id"]).first_or_404(
            description=f"Exercise with exercise_id {args['exercise_id']} does not exist"
        )

        if args["exercise_title"]:
            exercise.exercise_title = args["exercise_title"]
        if args["exercise_description"]:
            exercise.exercise_description = args["exercise_description"]
        if args["exercise_type"]:
            exercise.exercise_title = args["exercise_type"]
        if args["exercise_content"]:
            exercise.exercise_content = args["exercise_content"]

        db_engine.session.commit()

        result = dict(message=f"Successfully changed exercise with exercise_id {args['exercise_id']}")
        return utils.makeResponseNewCookie(result, 200, request.cookies)

    def delete(self) -> Response:
        """
        Implementation of the HTTP DELETE method. Use this method to delete an exercise by exercise_id.

        Returns:
             Response: Either a success message, or an error message as HTTP response.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="{error_msg}", required=True)

        args = parser.parse_args(strict=True)

        # check for access
        is_admin, auth, user_id = utils.authorize(cookies=request.cookies, method="DELETE", endpoint="exercise")
        if auth == None:
            return utils.makeResponseNewCookie(dict(message="Login required"), 401, request.cookies)
        elif not auth:
            return utils.makeResponseNewCookie(dict(message="No Access"), 403, request.cookies)

        # load the exercise table
        exercise_table = sqlalchemy.Table(config.EXERCISE_TABLE, db_engine.metadata, autoload=True)
        # compose the query to delete the requested element
        query = db_engine.delete(exercise_table).where(exercise_table.c.exercise_id == args["exercise_id"])

        # execute the query
        selection = db_engine.session.execute(query)
        db_engine.session.commit()
        # if no element was updated, the rowcount is 0
        if selection.rowcount == 0:
            result = dict(message=f"Exercise with exercise_id {args['exercise_id']} does not exist")
            return utils.makeResponseNewCookie(result, 404, request.cookies)

        result = dict(message=f"Successfully deleted exercise with exercise_id {args['exercise_id']}")
        return utils.makeResponseNewCookie(result, 200, request.cookies)
