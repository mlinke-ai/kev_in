#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib

from flask import Flask, Response, send_from_directory
from flask_restful import Api
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.core import config, errors
from backend.lib.interfaces import db_engine, UserModel
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
            self._sadmin_check()
        self.api = Api(self.app)
        self.api.add_resource(CourseResource, "/course")
        self.api.add_resource(ExerciseResource, "/exercise")
        self.api.add_resource(LoginResource, "/login")
        self.api.add_resource(UserResource, "/user")

    def _base(self) -> Response:
        return send_from_directory("../frontend/dist", "index.html")

    def _assets(self, path: str) -> Response:
        return send_from_directory("../frontend/dist", path)

    def _sadmin_check(self) -> None:
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        query = db_engine.select(user_table).select_from(user_table).where(user_table.c.user_name == config.SADMIN_NAME)
        selection = db_engine.session.execute(query)
        try:
            row = selection.scalar_one()
        except sqlalchemy.exc.NoResultFound:
            print("create sadmin")
            sadmin = UserModel(
                user_name=config.SADMIN_NAME,
                user_pass=hashlib.sha256(bytes(config.SADMIN_PASS, encoding="utf-8")).hexdigest(),
            )
            db_engine.session.add(sadmin)
            db_engine.session.commit()
        except sqlalchemy.exc.MultipleResultsFound:
            print("too many sadmins")
        else:
            print("exactly one sadmin")

    def run(self, debug: bool, host: bool) -> None:
        self.app.run(debug=debug, host="0.0.0.0" if host else "127.0.0.1")
