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

from flask import Response, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_restful import Resource, reqparse

from backend.database.models import UserModel, db


class LoginResource(Resource):
    def post(self) -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument("user_mail", type=str, help="{error_msg}", required=True)
        parser.add_argument("user_pass", type=str, help="{error_msg}", required=True)
        args = parser.parse_args(strict=True)
        query = db.select(UserModel).filter_by(user_mail=args["user_mail"])
        user = db.one_or_404(query, description="An user with this mail does not exist.")
        if user.verify(args["user_pass"]):
            token = create_access_token(identity=user.to_json())
            response = make_response(jsonify(dict(message=f"Welcome {user.user_name}!")), 200)
            set_access_cookies(response, token)
        else:
            response = make_response(jsonify(dict(message="Wrong credentials")), 401)
        return response
