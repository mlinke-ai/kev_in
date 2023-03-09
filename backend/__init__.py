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

import os

from flask import Flask, Response, send_from_directory
from flask_jwt_extended import JWTManager
from flask_restful import Api

from backend.config import configure_app
from backend.database.models import db
from backend.routes.exercise import ExerciseResource
from backend.routes.login import LoginResource
from backend.routes.logout import LogoutResource
from backend.routes.solution import SolutionResource
from backend.routes.user import UserResource
from backend.utils import refresh_token, revoked_token_check


def _get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))


def _get_instance_folder_path():
    return os.path.join(_get_app_base_path(), "instance")


def _base() -> Response:
    return send_from_directory("../frontend/dist", "index.html")


def _assets(path: str) -> Response:
    return send_from_directory("../frontend/dist", path)


def create_app(config: dict | str = dict()):
    app = Flask(
        __name__,
        instance_path=_get_instance_folder_path(),
        instance_relative_config=True,
    )
    configure_app(app, config)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.add_url_rule("/", "base", _base)
    app.add_url_rule("/<path:path>", "assets", _assets)
    jwt = JWTManager(app)
    jwt.token_in_blocklist_loader(revoked_token_check)
    app.after_request(refresh_token)
    api = Api(app)
    api.add_resource(UserResource, "/user", endpoint="user")
    api.add_resource(ExerciseResource, "/exercise", endpoint="exercise")
    api.add_resource(SolutionResource, "/solution", endpoint="solution")
    api.add_resource(LoginResource, "/login", endpoint="login")
    api.add_resource(LogoutResource, "/logout", endpoint="logout")
    return app


app = create_app()
