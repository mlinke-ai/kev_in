#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, jsonify, make_response
from flask_restful import Resource, reqparse


class Evaluator(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('exercise_id', type=str, required=True)
        parser.add_argument('user_solution', type=list(), required=True)

        exercise_id = parser.parse_args().get('exercise_id')

        # TODO:
        """ Decide on the basis of exercise_id which exercise type and how the evaluation
        must take place. Ask our database for "category", "test_args", "solution" """


