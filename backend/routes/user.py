#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, current_app, jsonify, make_response, request
from flask_jwt_extended import create_access_token, set_access_cookies, verify_jwt_in_request
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.database.models import UserModel, UserRole, db
from backend.utils import get_url, user_id_from_token


class UserResource(Resource):
    def __init__(self) -> None:
        # create a parser for the GET request data
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument("user_id", type=int, help="{error_msg}", location="args")
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
        Implementation of the HTTP GET method. Use this method to query the system for users

        Returns:
            Response: A HTTP response with all elements selected by the query in JSON or an error message.
        """
        args = self.get_parser.parse_args()

        query = db.select(UserModel).order_by(UserModel.user_id)
        if args["user_id"] is not None:
            query = query.where(UserModel.user_id == args["user_id"])
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
        Implementation of the HTTP POST method. Use this method to create a user.
        This method ensures uniqueness of the user.

        Returns:
            Response: A HTTP response with the newly created user.
        """
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
            token = create_access_token(identity=user.user_mail)
            response = make_response(jsonify(user.to_json()), 200)
            set_access_cookies(response, token)
            return response

    def put(self) -> Response:
        """
        Implementation of the HTTP PUT method. Use this method to change user attributes.
        This method ensures uniqueness of the user.

        Returns:
            Response: A HTTP response with the new user attributes.
        """
        # TODO: remove `optional` after debugging
        token = verify_jwt_in_request(optional=True)

        args = self.put_parser.parse_args(strict=True)

        if args["user_name"] == "":
            return make_response(jsonify(dict(message="user_name must not be empty")), 400)
        if args["user_mail"] == "":
            return make_response(jsonify(dict(message="user_mail must not be empty")), 400)
        if args["user_pass"] == "":
            return make_response(jsonify(dict(message="user_pass must not be empty")), 400)
        if args["user_role"] == UserRole.SAdmin:
            return make_response(jsonify(dict(message="No Access")), 403)

        query = db.select(UserModel).filter_by(user_id=args["user_id"])
        user = db.one_or_404(query, description="An user with this ID does not exist.")
        if args["user_name"]:
            user.user_name = args["user_name"]
        if args["user_mail"]:
            user.user_mail = args["user_mail"]
        if args["user_pass"]:
            user.user_pass = args["user_pass"]
        if args["user_role"]:
            user.user_role = args["user_role"]
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return make_response(jsonify(dict(message="An error occurred while updating the user")), 409)
        else:
            return make_response(jsonify(dict(message="Changed properties successfully")), 200)

    def delete(self) -> Response:
        """
        Implementation of the HTTP DELETE method. Use this method to delete a user.

        Returns:
            Response: A HTTP response with a success message.
        """
        # TODO: revoke token after self delete
        token = verify_jwt_in_request()
        args = self.delete_parser.parse_args(strict=True)
        query = db.select(UserModel).filter_by(user_id=args["user_id"])
        user = db.one_or_404(query, description="An user with this ID does not exist.")
        db.session.delete(user)
        db.session.commit()
        response = make_response(jsonify(dict(message="User deleted successfully")), 200)
        return response
