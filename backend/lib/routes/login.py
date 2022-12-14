#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy
import jwt
import hashlib

from backend.lib.interfaces.database import db_engine
from backend.lib.core import config


class LoginResource(Resource):
    def post(self) -> Response:
        """
        Implementation of HTTP POST method. Use this method to log in to an existing Account.
        The Post request needs two arguments: user_namme, user_pass.
        It is important to set 'Content-Type = application/json' in the header of the Request.

        Example Post Request (with default and passwort-hash):
        POST /login HTTP/1.1
        Host: 127.0.0.1:5000
        Content-Type: application/json
        Content-Length: 114

        {
            "user_name": "sadmin",
            "user_pass": "sadmin"
        }

        Arguments:
            user_name: account name of the user (required)
            user_pass: account passwort (required)

        Returns:
            HTTP-Response as JSON with an JWT token. (on success) 
            HTTP-Response as JSON with an error message. (on fail)
        """

        # create a parser for the request data and parse the request
        parser = reqparse.RequestParser()
        parser.add_argument("user_name", type=str, help="Name of the user is missing.", required=True)
        parser.add_argument("user_pass", type=str, help="Credentials of the user are missing.", required=True)
        args = parser.parse_args()
        #hash the password with sha-256
        args["user_pass"] = hashlib.sha256(bytes(args["user_pass"], encoding="utf-8")).hexdigest()
        # load the user table
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        # compose a query to select the requested element
        query = (
            db_engine.select(user_table)
            .select_from(user_table)
            .where(user_table.c.user_name == args["user_name"])
            .where(user_table.c.user_pass == args["user_pass"])
        )
        result = dict()
        # execute the query and store the selection
        selection = db_engine.session.execute(query)
        try:
            user = selection.one()
        except sqlalchemy.exc.NoResultFound as e:
            result = dict(message="Incorrect user name or password")
            return make_response(jsonify(result), 401)
        else:
            token = jwt.encode({"user_id": user[0]}, config.JWT_KEY)
            result = dict(token=token)

        return make_response(jsonify(result), 200)
