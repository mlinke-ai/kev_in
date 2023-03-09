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
