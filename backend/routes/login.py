#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
            token = create_access_token(identity=user.user_mail)
            response = make_response(jsonify(dict(message=f"Welcome {user.user_name}!")), 200)
            set_access_cookies(response, token)
        else:
            response = make_response(jsonify(dict(message="Wrong credentials")), 401)
        return response
