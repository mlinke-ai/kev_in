#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, current_app, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, verify_jwt_in_request
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

        result = list()
        stmt = sqlalchemy.select(UserModel).order_by(UserModel.user_id)
        with Session(db) as session:
            selection = session.execute(stmt)
            for user in selection.scalars():
                result.append(
                    dict(
                        user_id=user.user_id,
                        user_name=user.user_name,
                        user_mail=user.user_mail,
                        user_role=user.user_role,
                    )
                )
        return make_response(jsonify(dict(data=result, size=len(result))), 200)

    def post(self) -> Response:
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, help="{error_msg}", required=True)
        parser.add_argument("user_pass", type=str, help="{error_msg}", required=True)
        parser.add_argument("user_mail", type=str, help="{error_msg}", required=True)

        args = parser.parse_args(strict=True)

        if args["user_name"] == "":
            return make_response(jsonify(dict(message="user_name must not be empty")), 400)
        if args["user_pass"] == "":
            return make_response(jsonify(dict(message="user_pass must not be empty")), 400)
        if args["user_mail"] == "":
            return make_response(jsonify(dict(message="user_mail must not be empty")), 400)

        user = UserModel(args["user_name"], args["user_pass"], args["user_mail"])
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return make_response(dict(message="An user with this mail does already exist"), 409)
        else:
            token = create_access_token(identity=user.user_mail)
            response = make_response(jsonify(user.to_json()), 200)
            set_access_cookies(response, token)
            return response

    def put(self) -> Response:
        token = verify_jwt_in_request()
        print(token)

    def delete(self) -> Response:
        token = verify_jwt_in_request()
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, help="{error_msg}", required=True)
        args = parser.parse_args(strict=True)
        query = db.select(UserModel).filter_by(user_id=args["user_id"])
        user = db.one_or_404(query, description="An user with this ID does not exist.")
        db.session.delete(user)
        db.session.commit()
        response = make_response(jsonify(dict(message="User deleted successfully")), 200)
        return response
