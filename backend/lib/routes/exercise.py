#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.interfaces.database import ExerciseModel, db_engine
from backend.lib.core import config, utils


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
            location="args"
        )
        parser.add_argument("exercise_content", type=str, help="{error_msg}", location="args")
        parser.add_argument("exercise_offset", type=int, default=0, help="{error_msg}", location="args")
        parser.add_argument("exercise_limit", type=int, default=config.MAX_ITEMS_RETURNED, help="{error_msg}", location="args")

        args = parser.parse_args()

        # check if page limit is in range
        if args["exercise_limit"] not in range(config.MAX_ITEMS_RETURNED + 1):
            return make_response(
                jsonify(dict(message="Page limit not in range", min_limit=0, max_limit=config.MAX_ITEMS_RETURNED), 400)
            )

        #check for access
        auth = utils.authorize(
            cookies= request.cookies,
            method= "GET",
            endpoint= "exercise"
            )
        if auth == None:
            return make_response((jsonify(dict(message="Login required"))), 401)
        elif not auth:
            return make_response((jsonify(dict(message="No Access"))), 403)

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
        result = dict()
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        for row in selection.fetchall():

            result[int(row["exercise_id"])] = dict(
                exercise_id=int(row["exercise_id"]),
                exercise_title=str(row["exercise_title"]),
                exercise_description=str(row["exercise_description"]),
                exercise_type=row["exercise_type"].name,
                exercise_content=str(row["exercise_content"]),
            )

        return make_response((jsonify(result)), 200)

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
            required=True
        )
        parser.add_argument("exercise_content", type=str, help="{error_msg}", required=True)

        args = parser.parse_args()

        #check for access
        auth = utils.authorize(
            cookies= request.cookies,
            method= "POST",
            endpoint= "exercise"
            )
        if auth == None:
            return make_response((jsonify(dict(message="Login required"))), 401)
        elif not auth:
            return make_response((jsonify(dict(message="No Access"))), 403)

        # load the exercise table
        exercise_table = sqlalchemy.Table(config.EXERCISE_TABLE, db_engine.metadata, autoload=True)
        # compose the query
        query = db_engine.select([sqlalchemy.func.count()]).select_from(exercise_table)
        if args["exercise_title"]:
            query = query.where(exercise_table.c.exercise_title == args["exercise_title"])
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # check wether the selection contains an element
        if selection.scalar() == 0:
            # if the selection contains no elements it means we can safely create the new element
            # create a new element
            exercise = ExerciseModel(
                exercise_title=args["exercise_title"],
                exercise_description=args["exercise_description"],
                exercise_type=args["exercise_type"],
                exercise_content=args["exercise_content"],
            )
            # add the new element
            db_engine.session.add(exercise)
            db_engine.session.commit()
            # compose a query to check wether the new element was added successfully
            # TODO: query for last created element not based on given parameters
            query = (
                db_engine.select([exercise_table.c.exercise_title, exercise_table.c.exercise_id])
                .select_from(exercise_table)
                .where(exercise_table.c.exercise_title == args["exercise_title"])
            )
            # execute the query and store the result
            selection = db_engine.session.execute(query)
            try:
                # get the only element from the selection
                row = selection.fetchone()
            except sqlalchemy.exc.NoResultFound:
                # if there is no element the element could not be added
                result = dict(message="An error occurred while creating the exercise")
                return make_response((jsonify(result)), 500)
            else:
                result = dict(
                    message="The exercise was created successfully",
                    exercise_title=row.exercise_title,
                    exercise_id=row.exercise_id,
                )
                return make_response((jsonify(result)), 201)
        else:
            # if the selection contains an element we can't create a new one as we would create a duplicate
            result = dict(message="An exercise with this title already exists")
            return make_response((jsonify(result)), 409)
        # return the new element (importend for the ID) or an error message

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change an exercise.
        All given Attributes will be chagned. (except for exercise_id)

        Returns:
            Response: Either a success message, or an error message as HTTP response.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="{error_msg}", required=True)
        parser.add_argument("exercise_title", type=str, help="{error_msg}")
        parser.add_argument("exercise_description", type=str, help="{error_msg}")
        parser.add_argument("exercise_type", type=lambda x: config.ExerciseType(int(x)), help="{error_msg}")
        parser.add_argument("exercise_content", type=str, help="{error_msg}")

        args = parser.parse_args()

        #check for access
        auth = utils.authorize(
            cookies= request.cookies,
            method= "PUT",
            endpoint= "exercise"
            )
        if auth == None:
            return make_response((jsonify(dict(message="Login required"))), 401)
        elif not auth:
            return make_response((jsonify(dict(message="No Access"))), 403)

        # load the exercise table
        exercise_table = sqlalchemy.Table(config.EXERCISE_TABLE, db_engine.metadata, autoload=True)
        # drop the ID as we don't want to update it
        values = args.copy()
        del values["exercise_id"]
        # compose the query to update the requested element
        query = (
            db_engine.update(exercise_table).where(exercise_table.c.exercise_id == args["exercise_id"]).values(values)
        )
        # execute the query
        selection = db_engine.session.execute(query)
        db_engine.session.commit()
        # if no element was updated, the rowcount is 0
        if selection.rowcount == 0:
            result = dict(message=f"Exercise with exercise_id {args['exercise_id']} does not exist")
            return make_response((jsonify(result)), 404)

        result = dict(message=f"Successfully chanaged exercise with exercise_id {args['exercise_id']}")
        return make_response((jsonify(result)), 200)

    def delete(self) -> Response:
        """
        Implementation of the HTTP DELETE method. Use this method to delete an exercise by exercise_id.

        Returns:
             Response: Either a success message, or an error message as HTTP response.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="{error_msg}", required=True)

        args = parser.parse_args()

        #check for access
        auth = utils.authorize(
            cookies= request.cookies,
            method= "DELETE",
            endpoint= "exercise"
            )
        if auth == None:
            return make_response((jsonify(dict(message="Login required"))), 401)
        elif not auth:
            return make_response((jsonify(dict(message="No Access"))), 403)

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
            return make_response((jsonify(result)), 404)

        result = dict(message=f"Successfully deleted exercise with exercise_id {args['exercise_id']}")
        return make_response((jsonify(result)), 200)

