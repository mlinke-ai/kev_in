#!/usr/bin/env python3
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

import hashlib

import jwt
from flask import Response, current_app, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.interfaces.database import UserModel


class LoginResource(Resource):
    def post(self) -> Response:
        """
        Implementation of HTTP POST method. Use this method to log in to an existing Account.
        The Post request needs two arguments: user_name, user_pass.
        It is important to set 'Content-Type = application/json' in the header of the Request.

        Example Post Request (with default and passwort-hash):
        POST /login HTTP/1.1
        Host: 127.0.0.1:5000
        Content-Type: application/json
        Content-Length: 114

        {
            "user_mail": "sadmin@example.com",
            "user_pass": "sadmin"
        }

        Arguments:
            user_mail: account mail-address (required)
            user_pass: account passwort (required)

        Returns:
            HTTP-Response as JSON with a success message and the token in a cookie. (on success) -> status 200
            HTTP-Response as JSON with an error message. (on fail) -> status 401
        """

        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_mail", type=str, help="{error_msg}", required=True)
        parser.add_argument("user_pass", type=str, help="{error_msg}", required=True)
        args = parser.parse_args(strict=True)

        # hash the password with sha-256
        args["user_pass"] = hashlib.sha256(bytes(args["user_pass"], encoding="utf-8")).hexdigest()

        try:
            user: UserModel = UserModel.query.filter_by(user_mail=args["user_mail"], user_pass=args["user_pass"]).one()
        except sqlalchemy.exc.NoResultFound:
            result = dict(message="Incorrect user name or password")
            return make_response(jsonify(result), 401)
        else:
            token = jwt.encode({"user_id": user.user_id}, current_app.config["JWT_SECRET"])
            result = user.to_json()
            result["message"] = f"Welcome {user.user_name}!"
            response = make_response(jsonify(result), 200)
            response.set_cookie("token", token, max_age=3600, httponly=True)
            return response
