#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.interfaces.database import ExerciseModel, db_engine


class ExerciseResource(Resource):
    def get(self) -> dict:
        """Implementation of the HTTP GET method. Use this method to query the system for exercises.
        TODO: add explanation of all request fields

        Returns:
            dict: All elements selected by the query in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="ID of the exercise is missing")
        # TODO: add more exercise properties
        args = parser.parse_args()
        # load the exercise table
        exercise_table = sqlalchemy.Table("exercise_model", db_engine.metadata, autoload=True)
        # compose a query to select the requested element
        query = db_engine.select(exercise_table).select_from(exercise_table)
        if args["exercise_id"]:
            query = query.where(exercise_table.c.exercise_id == args["exercise_id"])
        result = dict()
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        # load the selection into the response data
        for row in selection.fetchall():
            result[row[0]] = dict(exercise_id=row[0])
        return result

    def post(self) -> dict:
        """Implementation of the HTTP POST method. Use this method to create a new exercise. This method prevents duplications.
        TODO: add explanation of all request fields

        Returns:
            dict: Either the new element or an error message in JSON.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_title", type=str, help="Title of the exercise is missing")
        # TODO: add more exercise properties
        args = parser.parse_args()
        # load the exercise table
        exercise_table = sqlalchemy.Table("exercise_model", db_engine.metadata, autoload=True)
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
            # compose a query to check wether the new element was added successfully
            # TODO: query for last created element not based on given parameters
            query = (
                db_engine.select([exercise_table.c.exercise_title])
                .select_from(exercise_table)
                .where(exercise_table.c.exercise_title == args["exercise_title"])
            )
            # execute the query and store the result
            selection = db_engine.session.execute(query)
            try:
                # get the only element from the selection
                row = selection.scalar_one()
            except sqlalchemy.exec.NoResultFound:
                # if there is no element the element could not be added
                result = dict(message="An error occurred while creating the exercise")
            else:
                # if the element got added commit the changes
                db_engine.session.commit()
                result = dict(
                    message="The exercise was created successfully",
                    exercise_title=row.exercise_title,
                    exercise_id=row.exercise_id,
                )
        else:
            # if the selection contains an element we can't create a new one as we would create a duplicate
            result = dict(message="A exercise with this title already exists")
        # return the new element (importend for the ID) or an error message
        return result

    def put(self) -> dict:
        """Implementation of the HTTP PUT method. Use this method to change an exercise.
        TODO: add explanation of all request fields

        Returns:
            dict: TODO: add return message
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="ID of the exercise is missing", required=True)
        parser.add_argument("exercise_title", type=str, help="Title of the exercise is missing")
        # TODO: add more exercise properties
        args = parser.parse_args()
        # load the exercise table
        exercise_table = sqlalchemy.Table("exercise_model", db_engine.metadata, autoload=True)
        # drop the ID as we don't want to update it
        values = args.copy()
        del values["exercise_id"]
        # compose the query to update the requested element
        query = (
            db_engine.update(exercise_table).wehre(exercise_table.c.exercise_id == args["exercise_id"]).values(values)
        )
        result = dict()
        # execute the query (the selection is not needed)
        selection = db_engine.session.execute(query)
        db_engine.session.commit()
        return result

    def delete(self) -> dict:
        """Implementation of the HTTP DELETE method. Use this method to delete an exercise.
        TODO: add explanation of all request fields

        Returns:
            dict: TODO: add return message
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("exercise_id", type=int, help="ID of the exercise is missing", required=True)
        # TODO: do we really need any other argument besides the ID?
        parser.add_argument("exercise_title", type=str, help="Title of the exercise is missing")
        args = parser.parse_args()
        # load the exercise table
        exercise_table = sqlalchemy.Table("exercise_model", db_engine.metadata, autoload=True)
        # compose the query to delete the requested element
        query = db_engine.delete(exercise_table).where(exercise_table.c.exercise_id == args["exercise_id"])
        if args["exercise_title"]:
            query = query.where(exercise_table.c.exercise_title == args["exercise_title"])
        result = dict()
        # execute the query (the selection is not needed)
        selection = db_engine.session.execute(query)
        db_engine.session.commit()
        return result