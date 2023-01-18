#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

from flask import Flask, Response, send_from_directory
from flask_restful import Api
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.core import config
from backend.lib.interfaces import UserModel, db_engine
from backend.lib.routes import (ExerciseResource, LoginResource,
                                SolutionResource, UserResource)


class Server:
    def __init__(self, database_uri) -> None:
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "base", self._base)
        self.app.add_url_rule("/<path:path>", "assets", self._assets)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
        with self.app.app_context():
            db_engine.init_app(self.app)
            db_engine.create_all()
            self._sadmin_check()
            self._tuser_check()
        self.api = Api(self.app)
        self.api.add_resource(ExerciseResource, "/exercise")
        self.api.add_resource(LoginResource, "/login")
        self.api.add_resource(UserResource, "/user")
        self.api.add_resource(SolutionResource, "/solution")

    def _base(self) -> Response:
        return send_from_directory("../frontend/dist", "index.html")

    def _assets(self, path: str) -> Response:
        return send_from_directory("../frontend/dist", path)

    def _sadmin_check(self) -> None:
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        query = (
            db_engine.select(user_table).select_from(user_table).where(user_table.c.user_role == config.UserRole.SAdmin)
        )
        selection = db_engine.session.execute(query)
        try:
            row = selection.scalar_one()
        except sqlalchemy.exc.NoResultFound:
            print("create sadmin")
            sadmin = UserModel(
                user_name=config.SADMIN_NAME,
                user_pass=hashlib.sha256(bytes(config.SADMIN_PASS, encoding="utf-8")).hexdigest(),
                user_mail=config.SADMIN_MAIL,
                user_role=config.UserRole.SAdmin,
            )
            db_engine.session.add(sadmin)
            db_engine.session.commit()
        except sqlalchemy.exc.MultipleResultsFound:
            print("too many sadmins")
        else:
            print("exactly one sadmin")

    def _tuser_check(self) -> None:
        user_table = sqlalchemy.Table(config.USER_TABLE, db_engine.metadata, autoload=True)
        query = db_engine.select(user_table).select_from(user_table).where(user_table.c.user_name == config.TUSER_NAME)
        selection = db_engine.session.execute(query)
        try:
            row = selection.scalar_one()
        except sqlalchemy.exc.NoResultFound:
            print("create tuser")
            tuser = UserModel(
                user_name=config.TUSER_NAME,
                user_pass=hashlib.sha256(bytes(config.TUSER_PASS, encoding="utf-8")).hexdigest(),
                user_mail=config.TUSER_MAIL,
                user_role=config.UserRole.User,
            )
            db_engine.session.add(tuser)
            db_engine.session.commit()
        except sqlalchemy.exc.MultipleResultsFound:
            print("too many tusers")
        else:
            print("exactly one tuser")

    def run(self, debug: bool = False, host: bool = False) -> None:
        self.app.run(debug=debug, host="0.0.0.0" if host else "127.0.0.1")


if __name__ == "__main__":
    raise RuntimeError("The server is mend to be run from a run script. Do not run in standalone.")
