#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from flask import Flask, Response, send_from_directory
from flask_restful import Api

from backend.lib.core import config, errors
from backend.lib.interfaces import db_engine
from backend.lib.routes import CourseResource, ExerciseResource, LoginResource, UserResource


class Server:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "base", self._base)
        self.app.add_url_rule("/<path:path>", "assets", self._assets)
        if os.environ.get("SQLALCHEMY_DATABASE_URI", None) == None:
            self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        with self.app.app_context():
            db_engine.init_app(self.app)
            db_engine.create_all()

        self.api = Api(self.app)
        self.api.add_resource(CourseResource, "/course")
        self.api.add_resource(ExerciseResource, "/exercise")
        self.api.add_resource(LoginResource, "/login")
        self.api.add_resource(UserResource, "/user")

    def _base(self) -> Response:
        return send_from_directory("../frontend/dist", "index.html")

    def _assets(self, path: str) -> Response:
        return send_from_directory("../frontend/dist", path)

    def run(self, debug: bool) -> None:
        self.app.run(debug=debug)
