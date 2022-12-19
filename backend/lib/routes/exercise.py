#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jwt

from flask import Response, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.interfaces.database import ExerciseModel, db_engine
from backend.lib.core import config


class ExerciseResource(Resource):
    def get(self) -> Response:
        """Implementation of the HTTP GET method. Use this method to query the system for exercises.
        TODO: add explanation of all request fields

        Returns:
            Response: A HTTP response with all selected items in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="ID of the exercise is missing", location="args")
        #watch for the JWT in the header
        parser.add_argument("Authorization", type=str, help="no JSON Web Token was sent", location="headers")
        # TODO: add more exercise properties
        args = parser.parse_args()

        #check if the client has access
        if args["Authorization"]:
            if not self._authorize(args["Authorization"]):
                return make_response((jsonify(dict(message="No Access."))), 403)
        else:
            return make_response((jsonify(dict(message="Login required."))), 401)
        
        # load the exercise table
        exercise_table = sqlalchemy.Table(config.EXERCISE_TABLE, db_engine.metadata, autoload=True)
        # compose a query to select the requested element
        query = db_engine.select(exercise_table).select_from(exercise_table)
        if args["exercise_id"]:
            query = query.where(exercise_table.c.exercise_id == args["exercise_id"])
        result = dict()
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        for row in selection.fetchall():
            result[row[0]] = dict(exercise_id=row[0],exercise_title=row[1])
        return make_response((jsonify(result)), 200)

    def post(self) -> Response:
        """Implementation of the HTTP POST method. Use this method to create a new exercise. This method prevents duplications.
        TODO: add explanation of all request fields

        Returns:
            Response: Either the new element or an error message in JSON as HTTP response.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_title", type=str, help="Title of the exercise is missing")
        #watch for the JWT in the header
        parser.add_argument("Authorization", type=str, help="no JSON Web Token was sent", location="headers")
        # TODO: add more exercise properties
        args = parser.parse_args()

        #check if the client has access
        if args["Authorization"]:
            if not self._authorize(args["Authorization"]):
                return make_response((jsonify(dict(message="No Access."))), 403)
        else:
            return make_response((jsonify(dict(message="Login required."))), 401)

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
            exercise = ExerciseModel(exercise_title=args["exercise_title"])
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
        """Implementation of the HTTP PUT method. Use this method to change an exercise.
        TODO: add explanation of all request fields

        Returns:
            Response: Either a success message, or an error message as HTTP response.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="ID of the exercise is missing", required=True)
        parser.add_argument("exercise_title", type=str, help="Title of the exercise is missing")
        #watch for the JWT in the header
        parser.add_argument("Authorization", type=str, help="no JSON Web Token was sent", location="headers")
        # TODO: add more exercise properties
        args = parser.parse_args()

        #check if the client has access
        if args["Authorization"]:
            if not self._authorize(args["Authorization"]):
                return make_response((jsonify(dict(message="No Access."))), 403)
        else:
            return make_response((jsonify(dict(message="Login required."))), 401)

        # load the exercise table
        exercise_table = sqlalchemy.Table(config.EXERCISE_TABLE, db_engine.metadata, autoload=True)
        # drop the ID and Authorization header value as we don't want to update it
        values = args.copy()
        del values["exercise_id"]
        del values["Authorization"]
        # compose the query to update the requested element
        query = (
            db_engine.update(exercise_table).where(exercise_table.c.exercise_id == args["exercise_id"]).values(values)
        )
        # execute the query (the selection is not needed)
        selection = db_engine.session.execute(query)
        print(selection.rowcount)
        db_engine.session.commit()
        #if no element was updated, the rowcount is 0
        if selection.rowcount == 0:
            result = dict(message=f"Exercise with exercise_id {args['exercise_id']} does not exist")
            return make_response((jsonify(result)), 404)

        result = dict(message=f"Successfully chanaged exercise with exercise_id {args['exercise_id']}")
        return make_response((jsonify(result)), 200)

    def delete(self) -> Response:
        """Implementation of the HTTP DELETE method. Use this method to delete an exercise.
        TODO: add explanation of all request fields

        Returns:
             Response: Either a success message, or an error message as HTTP response.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="ID of the exercise is missing", required=True)
        # TODO: do we really need any other argument besides the ID?
        parser.add_argument("exercise_title", type=str, help="Title of the exercise is missing")
        #watch for the JWT in the header
        parser.add_argument("Authorization", type=str, help="no JSON Web Token was sent", location="headers")
        args = parser.parse_args()

        if args["Authorization"]:
            if not self._authorize(args["Authorization"]):
                return make_response((jsonify(dict(message="No Access."))), 403)
        else:
            return make_response((jsonify(dict(message="Login required."))), 401)

        # load the exercise table
        exercise_table = sqlalchemy.Table(config.EXERCISE_TABLE, db_engine.metadata, autoload=True)
        # compose the query to delete the requested element
        query = db_engine.delete(exercise_table).where(exercise_table.c.exercise_id == args["exercise_id"])
        if args["exercise_title"]:
            query = query.where(exercise_table.c.exercise_title == args["exercise_title"])
        
        # execute the query (the selection is not needed)
        selection = db_engine.session.execute(query)
        db_engine.session.commit()
        #if no element was updated, the rowcount is 0
        if selection.rowcount == 0:
            result = dict(message=f"Exercise with exercise_id {args['exercise_id']} does not exist")
            return make_response((jsonify(result)), 404)

        result = dict(message=f"Successfully deleted exercise with exercise_id {args['exercise_id']}")
        return make_response((jsonify(result)), 200)

    def _authorize(self, authHeaderVal: str) -> bool:
        """
        This method is used to determine if a certain client has the right to change or access data, based on the
        HTTP request. Therefore the JWT is decoded. Returns true if access is granted and false when access is denied
        TODO distinguish between read and write/delete (so POST, PUT, DELETE should be treated differently)
        """
        
        #authHeaderVal should be 'Bearer <token>' like in the JWT standard
        values = authHeaderVal.split(" ")
        if values[0] != "Bearer":
            return False #wrong format
        try:
            token = values[1]
        except IndexError:
            return False #wrong format
        
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
            return True