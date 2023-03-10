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

import json
import random

import flask_sqlalchemy

from backend.lib.core import config

db_engine = flask_sqlalchemy.SQLAlchemy()


class UserModel(db_engine.Model):
    __tablename__ = config.USER_TABLE
    user_id = db_engine.Column(db_engine.Integer, primary_key=True)
    user_name = db_engine.Column(db_engine.String)
    user_pass = db_engine.Column(db_engine.String(64))
    user_mail = db_engine.Column(db_engine.String, unique=True)
    user_role = db_engine.Column(db_engine.Enum(config.UserRole))

    def to_json(self) -> dict:
        return dict(
            user_id=self.user_id,
            user_name=self.user_name,
            user_mail=self.user_mail,
            user_role_name=self.user_role.name,
            user_role_value=self.user_role.value,
        )


class ExerciseModel(db_engine.Model):
    __tablename__ = config.EXERCISE_TABLE
    exercise_id = db_engine.Column(db_engine.Integer, primary_key=True)
    exercise_title = db_engine.Column(db_engine.String, unique=True)
    exercise_description = db_engine.Column(db_engine.String)
    exercise_type = db_engine.Column(db_engine.Enum(config.ExerciseType))
    exercise_content = db_engine.Column(db_engine.Text)
    exercise_solution = db_engine.Column(db_engine.Text)
    exercise_language = db_engine.Column(db_engine.Enum(config.ExerciseLanguage))

    def to_json(self, details: bool, is_admin: bool) -> dict:
        if details:
            return dict(
                exercise_id=self.exercise_id,
                exercise_title=self.exercise_title,
                exercise_description=self.exercise_description,
                exercise_type_name=self.exercise_type.name,
                exercise_type_value=self.exercise_type.value,
                exercise_content=prepareExerciseContent(json.loads(self.exercise_content), self.exercise_type),
                exercise_solution=json.loads(self.exercise_solution) if is_admin else "",
                exercise_language_name=self.exercise_language.name,
                exercise_language_value=self.exercise_language.value,
            )
        else:
            return dict(
                exercise_id=self.exercise_id,
                exercise_title=self.exercise_title,
                exercise_type_name=self.exercise_type.name,
                exercise_type_value=self.exercise_type.value,
                exercise_language_name=self.exercise_language.name,
                exercise_language_value=self.exercise_language.value,
            )


class SolutionModel(db_engine.Model):
    __tablename__ = config.SOLUTION_TABLE
    solution_id = db_engine.Column(db_engine.Integer, primary_key=True)
    solution_user = db_engine.Column(db_engine.Integer, db_engine.ForeignKey(UserModel.user_id))
    solution_exercise = db_engine.Column(db_engine.Integer, db_engine.ForeignKey(ExerciseModel.exercise_id))
    solution_date = db_engine.Column(db_engine.DateTime)
    solution_duration = db_engine.Column(db_engine.Interval)
    solution_correct = db_engine.Column(db_engine.Boolean)
    solution_pending = db_engine.Column(db_engine.Boolean)
    solution_content = db_engine.Column(db_engine.Text)
    user_relation = db_engine.relationship(UserModel, foreign_keys="SolutionModel.solution_user")
    exercise_relation = db_engine.relationship(ExerciseModel, foreign_keys="SolutionModel.solution_exercise")

    def to_json(self) -> dict:
        return dict(
            solution_id=self.solution_id,
            solution_user=self.solution_user,
            solution_exercise=self.solution_exercise,
            solution_date=self.solution_date,
            solution_duration=int(self.solution_duration.total_seconds()),
            solution_correct=self.solution_correct,
            solution_pending=self.solution_pending,
            solution_content=json.loads(self.solution_content),
        )


# moved this from utils.py to database.py because I cannot import utils here (circular import)
# maybe we can find a better place for this
def prepareExerciseContent(exerciseContent: dict, exerciseType: config.ExerciseType) -> dict:
    """
    Before sending out the exercise content via GET, some preperations have to be done for some exercise types. This
    method implements these preperations.
    """

    newContent = exerciseContent

    if exerciseType == config.ExerciseType.ParsonsPuzzleExercise:
        newContent = _randomizePPEContent(exerciseContent)

    if newContent == None:
        return exerciseContent  # preperation failed, just returns default exerciseContent
    return newContent


def _randomizePPEContent(content: dict[str, list]) -> dict[str, list] | None:
    """
    Takes the `exercise_content` argument from a parsons puzzle exercise and randomizes the list, which is stored
    under the "list" key.
    """

    try:
        data = content["list"]
    except KeyError:
        return None
    if not isinstance(data, list):
        return None
    random.shuffle(data)
    content["list"] = data

    return content
