#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, jsonify, make_response
from flask_jwt_extended import get_jti, verify_jwt_in_request
from flask_restful import Resource
from flask_sqlalchemy.query import sqlalchemy

from backend.database.models import BlocklistModel, db


class LogoutResource(Resource):
    def delete(self) -> Response:
        token = verify_jwt_in_request()
        jti = get_jti(token[1])
        blocklist = BlocklistModel(jti)
        db.session.add(blocklist)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            return make_response(jsonify(dict(message="An error occurred while logging out.")), 500)
        else:
            response = make_response(jsonify(dict()), 200)
            response.delete_cookie("jwt_access_token")
            response.delete_cookie("csrf_access_token")
            return response
