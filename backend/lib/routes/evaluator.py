#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, jsonify, make_response
from flask_restful import Resource, reqparse
from backend.lib.sandbox.pyenv.pysandbox import ExecutePython


class EvaluatorResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('exercise_id', type=str, required=True)
        parser.add_argument('user_result', type=list(), required=True)

        exercise_id = parser.parse_args().get('exercise_id')

        # TODO:
        """ Decide on the basis of exercise_id which exercise type and how the evaluation
        must take place. Ask our database for "category", "user_func", "test_args", "solution" """

        """" python evaluator """""
        user_code = parser.parse_args().get('user_result')

        # user_func = "multiplicate"
        user_func = "fib"
        # user_func = "reverse_for_loop"

        myTest = TestClass(user_func)
        myTest.generate_input_data()
        pythonEvaluator = ExecutePython()
        sandbox_log = pythonEvaluator.exec_untrusted_code(user_code=user_code, user_func=user_func, *myTest.test_args)

        if not sandbox_log["RESULTLOG"]:
            # execute user code failed
            response = None
            if sandbox_log["EXECUTELOG"]:
                # execution error
                response = sandbox_log["EXECUTELOG"]
            else:
                # interpreter error
                response = sandbox_log["COMPILERLOG"]
            return make_response(jsonify(response), 200)

        if sandbox_log["RESULTLOG"] == myTest.input_data:
            pass


class TestClass:

    def __init__(self, user_func):
        self.user_func = user_func
        self.test_args = None
        self.input_data = dict()

    def generate_input_data(self):
        if self.user_func == "fib":
            # fibonacci
            self.input_data["0"] = ([0], [0])
            self.input_data["1"] = ([1], [1])
            self.input_data["2"] = ([7], [13])
        elif self.user_func == "reverse_for_loop":
            # reverseStringLoop
            self.input_data = dict()
            self.input_data["0"] = (['"Hello World"'], ['dlroW olleH'])
            self.input_data["1"] = (['"Kev.in"'], ['ni.veK'])
        elif self.user_func == "multiplicate":
            # multiplication
            self.input_data = dict()
            self.input_data["0"] = ([2, 2, 2], [8])
        else:
            return

        self.test_args = [args[0] for args in self.input_data.values()]
