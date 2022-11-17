#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os

from flask import Flask, send_from_directory
from flask_restful import Api
from lib.core import config, errors
from lib.interfaces import db_engine
from lib.routes import Course, Exercise, Login, UserResource


def base():
    return send_from_directory("../frontend/public", "index.html")


def assets(path):
    return send_from_directory("../frontend/public", path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Kev.in Backend Server", description="The backend server of Kev.in exposing a REST API."
    )
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    app = Flask(__name__)
    app.add_url_rule("/", "base", base)
    app.add_url_rule("/<path:path>", "home", assets)
    if os.environ.get("SQLALCHEMY_DATABASE_URI", None) == None:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    with app.app_context():
        db_engine.init_app(app)
        db_engine.create_all()

    api = Api(app)
    api.add_resource(Course, "/course")
    api.add_resource(Login, "/login")
    api.add_resource(Exercise, "/exercise")
    api.add_resource(UserResource, "/user")

    app.run(debug=args.debug)
