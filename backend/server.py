#!/usr/bin/env python3
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

import datetime
import hashlib
import json
import secrets
import string

from flask import Flask, Response, send_from_directory
from flask_restful import Api
from flask_sqlalchemy.query import sqlalchemy

from backend.lib.core import config
from backend.lib.interfaces import ExerciseModel, SolutionModel, UserModel, db_engine
from backend.lib.routes import ExerciseResource, LoginResource, LogoutResource, SolutionResource, UserResource


class Server:
    def __init__(self, database_uri) -> None:
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "base", self._base)
        self.app.add_url_rule("/<path:path>", "assets", self._assets)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
        self.app.config["JWT_SECRET"] = self._gen_JWT_secret()
        with self.app.app_context():
            db_engine.init_app(self.app)
            db_engine.create_all()
            self._sadmin_check()
            self._tuser_check()
            self._gen_exercises()
            self._gen_solutions()
        self.api = Api(self.app)
        self.api.add_resource(ExerciseResource, "/exercise", endpoint="exercise")
        self.api.add_resource(LoginResource, "/login")
        self.api.add_resource(UserResource, "/user", endpoint="user")
        self.api.add_resource(SolutionResource, "/solution", endpoint="solution")
        self.api.add_resource(LogoutResource, "/logout")

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

    def _tuser_check(self) -> None:  # TODO should be removed for production
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

    def _gen_JWT_secret(self) -> str:
        # generate a random 64 letter password
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_"
        return "".join(secrets.choice(alphabet) for _ in range(64))

    def _gen_exercises(self) -> None:  # TODO should be removed for production
        # create some dummy exercises with different types
        exercise_table = sqlalchemy.Table(config.EXERCISE_TABLE, db_engine.metadata, autoload=True)
        query = db_engine.select(sqlalchemy.func.count()).select_from(exercise_table)
        selection = db_engine.session.execute(query)
        if selection.first()[0] < 50:
            print("create dummy exercises")
            for i in range(10):
                for j in range(7):
                    if j == 0:
                        content = {"text": "Dummy Text", "gap_positions": [1, 2, 3]}
                        solution = {"gap_entries": ["1", "2", "3"]}
                    elif j == 2:
                        content = {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
                        solution = {"list": ["Hello", "World", "this", "is", "the", "first", "exercise"]}
                    elif j == 6:
                        content = {"func": "multiply", "code": "def multiply(x, y):\r\npass"}
                        solution = {
                            "0": [[0, 0], [0]],
                            "1": [[1, 0], [0]],
                            "2": [[1, 2], [2]],
                            "3": [[2, 2], [4]],
                            "4": [[6, 7], [42]],
                            "5": [[-4, 5], [-20]],
                        }
                    else:
                        content = {}
                        solution = {}
                    exercise = ExerciseModel(
                        exercise_title=f"{config.ExerciseType(j + 1).name}{i}",
                        exercise_description=f"Dummy {config.ExerciseType(j + 1).name} number {i}",
                        exercise_type=config.ExerciseType(j + 1),
                        exercise_content=json.dumps(content),
                        exercise_solution=json.dumps(solution),
                        exercise_language=config.ExerciseLanguage.Python,
                    )
                    db_engine.session.add(exercise)
        else:
            print("found enough exercises")
        db_engine.session.commit()

    def _gen_solutions(self) -> None:  # TODO should be removed for production
        # create some dummy solutions: two for the first seven exercises (true and false)
        solution_table = sqlalchemy.Table(config.SOLUTION_TABLE, db_engine.metadata, autoload=True)
        query = db_engine.select(sqlalchemy.func.count()).select_from(solution_table)
        selection = db_engine.session.execute(query)
        if selection.first()[0] < 50:
            print("create dummy solutions")
            for i in range(7):
                content = {"solution": "some JSON"}
                solution = SolutionModel(
                    solution_user=1,
                    solution_exercise=i + 1,
                    solution_date=datetime.datetime.now(),
                    solution_duration=datetime.timedelta(minutes=3 * i, seconds=3 * i),
                    solution_correct=not i == 6,
                    solution_pending=i == 6,
                    solution_content=json.dumps(content),
                )
                db_engine.session.add(solution)
                solution = SolutionModel(
                    solution_user=i % 2 + 1,
                    solution_exercise=i + 1,
                    solution_date=datetime.datetime.fromtimestamp(1234567890),
                    solution_duration=datetime.timedelta(minutes=5 * i, seconds=5 * i),
                    solution_correct=False,
                    solution_pending=i == 6,
                    solution_content=json.dumps(content),
                )
                db_engine.session.add(solution)
        else:
            print("found enough solutions")
        db_engine.session.commit()

    def run(self, debug: bool = False, host: bool = False) -> None:
        self.app.run(debug=debug, host="0.0.0.0" if host else "127.0.0.1")


if __name__ == "__main__":
    raise RuntimeError("The server is mend to be run from a run script. Do not run in standalone.")
