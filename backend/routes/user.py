#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, current_app, jsonify, make_response, request
from flask_jwt_extended import create_access_token, set_access_cookies, verify_jwt_in_request
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.database.models import UserModel, UserRole, db
from backend.utils import get_url, user_id_from_token


class UserResource(Resource):
    def get(self) -> Response:
        """
        Implementation of the HTTP GET method. Use this method to query the system for users

        Returns:
            Response: A HTTP response with all elements selected by the query in JSON or an error message.
        """
        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, help="{error_msg}", location="args")
        parser.add_argument("user_name", type=str, help="{error_msg}", location="args")
        parser.add_argument("user_mail", type=str, help="{error_msg}", location="args")
        parser.add_argument(
            "user_role", type=lambda x: UserRole(int(x)), default=UserRole.User, help="{error_msg}", location="args"
        )
        parser.add_argument("user_page", type=int, default=1, help="{error_msg}", location="args")
        parser.add_argument(
            "user_limit",
            type=int,
            default=current_app.config["MAX_ITEMS_RETURNED"],
            help="{error_msg}",
            location="args",
        )

        args = parser.parse_args()

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
            db.session.rollback()
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
