#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from flask import Flask, Response, send_from_directory
from flask_jwt_extended import JWTManager
from flask_restful import Api

from backend.config import configure_app
from backend.database.models import db
from backend.routes.login import LoginResource
from backend.routes.logout import LogoutResource
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
    api.add_resource(LoginResource, "/login", endpoint="login")
    api.add_resource(LogoutResource, "/logout", endpoint="logout")
    return app


app = create_app()
