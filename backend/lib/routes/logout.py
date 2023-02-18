#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, make_response, jsonify
from flask_restful import Resource

class LogoutResource(Resource):

    def post(self) -> Response:

        response = make_response(jsonify({"message": "Successfully logged out."}), 200)
        response.set_cookie("token", max_age=0)

        return response
