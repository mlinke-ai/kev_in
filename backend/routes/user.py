#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, current_app, jsonify, make_response, request
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy
from flask_sqlalchemy.session import Session

from backend.database.models import UserModel, UserRole, db
from backend.utils import user_id_from_cookie


class UserResource(Resource):
    def get(self) -> Response:
        """
        Implementation of the HTTP GET method. Use this method to query the system for users

        Returns:
            Response: A HTTP response with all elements selected by the query in JSON or an error message.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, default=0, help="{error_msg}", location="args")
        parser.add_argument("user_name", type=str, default="", help="{error_msg}", location="args")
        parser.add_argument("user_mail", type=str, default="", help="{error_msg}", location="args")
        parser.add_argument(
            "user_role", type=lambda x: UserRole(int(x)), default=UserRole.User, help="{error_msg}", location="args"
        )
        parser.add_argument("user_offset", type=int, default=0, help="{error_msg}", location="args")
        parser.add_argument(
            "user_limit",
            type=int,
            default=current_app.config["MAX_ITEMS_RETURNED"],
            help="{error_msg}",
            location="args",
        )

        args = parser.parse_args()

        # check if page limit is in range
        if args["user_limit"] not in range(current_app.config["MAX_ITEMS_RETURNED"] + 1):
            return make_response(
                jsonify(
                    dict(
                        message="Page limit not in range",
                        min_limit=0,
                        max_limit=current_app.config["MAX_ITEMS_RETURNED"],
                    )
                ),
                400,
            )

        stmt = sqlalchemy.select(UserModel).order_by(UserModel.user_id)
        selection = db.session.execute(stmt)
        result = list()
        for user in selection.scalars():
            result.append(
                dict(user_id=user.user_id, user_name=user.user_name, user_mail=user.user_mail, user_role=user.user_role)
            )
        return make_response(jsonify(dict(data=result, size=len(result))), 200)
