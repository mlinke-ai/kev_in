#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy
import jwt

from backend.lib.interfaces.database import db_engine
from backend.lib.core import config


class LoginResource(Resource):
    def get(self) -> Response:
        # # create a parser for the request data and parse the request
        # parser = reqparse.RequestParser()
        # parser.add_argument("user_name", type=str, help="Name of the user is missing.", required=True)
        # parser.add_argument("user_pass", type=str, help="Credentials of the user are missing.", required=True)
        # args = parser.parse_args()
        # # load the user table
        # user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # # compose a query to select the requested element
        # query = (
        #     db_engine.select(user_table)
        #     .select_from(user_table)
        #     .where(user_table.c.user_name == args["user_name"])
        #     .where(user_table.c.user_cred == args["user_pass"])
        # )
        # result = dict()
        # # execute the query and store the selection
        # selection = db_engine.session.execute(query)
        # try:
        #     user = selection.one()
        # except sqlalchemy.exec.NoResultFound as e:
        #     result = dict(message="Incorrect user name or password")
        # else:
        #     token = jwt.encode({"user_id": user[0]})
        #     result = dict(token=token)
        # TODO: parse request
        # TODO: check for user (includes comparison of password hashes)
        # TODO: generate JWT token
        # TODO: serve token
        result = dict()
        return make_response(jsonify(result), status=200)
