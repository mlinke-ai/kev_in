#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, current_app, jsonify, make_response, request
from flask_jwt_extended import create_access_token, set_access_cookies, verify_jwt_in_request
from flask_restful import Resource, reqparse
from flask_sqlalchemy.query import sqlalchemy

from backend.database.models import UserModel, UserRole, db
from backend.utils import get_url, user_id_from_token


class SolutionResource(Resource):
    def __init__(self) -> None:
        pass

    def get(self) -> Response:
        pass

    def post(self) -> Response:
        pass

    def put(self) -> Response:
        pass

    def delete(self) -> Response:
        pass
