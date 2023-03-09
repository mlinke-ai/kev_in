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

from flask import Response, current_app, jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, set_access_cookies, verify_jwt_in_request
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.database.models import UserModel, UserRole, db
from backend.utils import get_url


class UserResource(Resource):
    def __init__(self) -> None:
        # create a parser for the GET request data
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("user_id", type=int, help="{error_msg}", action="append", location="args")
        self.get_parser.add_argument("user_name", type=str, help="{error_msg}", location="args")
        self.get_parser.add_argument("user_mail", type=str, help="{error_msg}", location="args")
        self.get_parser.add_argument(
            "user_role", type=lambda x: UserRole(int(x)), default=UserRole.User, help="{error_msg}", location="args"
        )
        self.get_parser.add_argument("user_page", type=int, default=1, help="{error_msg}", location="args")
        self.get_parser.add_argument(
            "user_limit",
            type=int,
            default=current_app.config["MAX_ITEMS_RETURNED"],
            help="{error_msg}",
            location="args",
        )
        # create a parser for the POST request data
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument("user_name", type=str, help="{error_msg}", required=True)
        self.post_parser.add_argument("user_pass", type=str, help="{error_msg}", required=True)
        self.post_parser.add_argument("user_mail", type=str, help="{error_msg}", required=True)
        # create a parser for the PUT request data
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument("user_id", type=int, help="{error_msg}", required=True)
        self.put_parser.add_argument("user_name", type=str, help="{error_msg}")
        self.put_parser.add_argument("user_mail", type=str, help="{error_msg}")
        self.put_parser.add_argument("user_pass", type=str, help="{error_msg}")
        self.put_parser.add_argument("user_role", type=lambda x: UserRole(int(x)), help="{error_msg}")
        # create a parser for the DELETE request data
        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument("user_id", type=int, help="{error_msg}", required=True)

    def get(self) -> Response:
        """
        Implementation of the HTTP GET method. Use this method to query the system for users.

        Returns:
            Response: A HTTP response with all elements selected by the query in JSON or an error message.
        """
        token = verify_jwt_in_request()

        args = self.get_parser.parse_args()

        if len(request.url.split("?")) == 1:
            return make_response(jsonify(get_jwt_identity()), 200)

        query = db.select(UserModel).order_by(UserModel.user_id)
        if args["user_id"] is not None:
            query = query.filter(UserModel.user_id.in_(args["user_id"]))
        if args["user_name"] is not None:
            query = query.where(UserModel.user_name == args["user_name"])
        if args["user_mail"] is not None:
            query = query.where(UserModel.user_mail == args["user_mail"])
        query = query.where(UserModel.user_role == args["user_role"])
        users = db.paginate(
            query,
            page=args["user_page"],
            per_page=args["user_limit"],
            max_per_page=current_app.config["MAX_ITEMS_RETURNED"],
        )

        if users.total == 0:
            return make_response(jsonify(dict()), 204)

        response = dict(data=list(), meta=dict())
        for user in users.items:
            response["data"].append(user.to_json())
        response["meta"]["total"] = users.total
        response["meta"]["next_page"] = users.next_num
        response["meta"]["prev_page"] = users.prev_num
        response["meta"]["next_url"] = get_url(request.url, user_page=users.next_num) if users.has_next else None
        response["meta"]["prev_url"] = get_url(request.url, user_page=users.prev_num) if users.has_prev else None
        response["meta"]["page_size"] = len(users.items)
        response["meta"]["pages"] = users.pages

        return make_response(jsonify(response), 200)

    def post(self) -> Response:
        """
        Implementation of the HTTP POST method. Use this method to create an user.
        This method ensures uniqueness of the user.

        Returns:
            Response: A HTTP response with the newly created user.
        """
        token = verify_jwt_in_request(optional=True)

        args = self.post_parser.parse_args(strict=True)

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
            db.session.rollback()
            return make_response(dict(message="An user with this mail does already exist"), 409)
        else:
            token = create_access_token(identity=user.to_json())
            response = make_response(jsonify(user.to_json()), 201)
            set_access_cookies(response, token)
            return response

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change user attributes.
        This method ensures uniqueness of the user.

        Returns:
            Response: A HTTP response with the new user attributes.
        """
        token = verify_jwt_in_request()

        args = self.put_parser.parse_args(strict=True)

        if args["user_name"] == "":
            return make_response(jsonify(dict(message="user_name must not be empty")), 400)
        if args["user_mail"] == "":
            return make_response(jsonify(dict(message="user_mail must not be empty")), 400)
        if args["user_pass"] == "":
            return make_response(jsonify(dict(message="user_pass must not be empty")), 400)
        if args["user_role"] == UserRole.SAdmin:
            return make_response(jsonify(dict(message="No Access")), 403)
        if args["user_role"] == UserRole.Admin and get_jwt_identity()["user_role_value"] == UserRole.User.value:
            return make_response(jsonify(dict(message="No Access")), 403)

        query = db.select(UserModel).filter_by(user_id=args["user_id"])
        user = db.one_or_404(query, description="An user with this ID does not exist.")
        if args["user_name"] is not None:
            user.user_name = args["user_name"]
        if args["user_mail"] is not None:
            user.user_mail = args["user_mail"]
        if args["user_pass"] is not None:
            user.user_pass = args["user_pass"]
        if args["user_role"] is not None:
            user.user_role = args["user_role"]
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return make_response(jsonify(dict(message="An user with this mail does already exist")), 409)
        else:
            return make_response(jsonify(dict(message="Changed properties successfully")), 200)

    def delete(self) -> Response:
        """
        Implementation of the HTTP DELETE method. Use this method to delete an user.

        Returns:
            Response: A HTTP response with a success message.
        """
        token = verify_jwt_in_request()

        args = self.delete_parser.parse_args(strict=True)

        if (
            get_jwt_identity()["user_id"] == args["user_id"]
            or get_jwt_identity()["user_role_value"] != UserRole.User.value
        ):
            query = db.select(UserModel).filter_by(user_id=args["user_id"])
            user = db.one_or_404(query, description="An user with this ID does not exist.")
            db.session.delete(user)
            db.session.commit()
            response = make_response(jsonify(dict(message="User deleted successfully")), 200)
        else:
            response = make_response(jsonify(dict(message="Users are not authorized to perform this action.")), 403)
        return response
