#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask_sqlalchemy
import enum

from backend.lib.core import errors, config

db_engine = flask_sqlalchemy.SQLAlchemy()


class UserModel(db_engine.Model):
    __tablename__ = config.USER_TABLE
    user_id = db_engine.Column(db_engine.Integer, primary_key=True)
    user_name = db_engine.Column(db_engine.String)
    user_pass = db_engine.Column(db_engine.String(64))
    user_mail = db_engine.Column(db_engine.String, unique=True)
    user_role = db_engine.Column(db_engine.Enum(config.UserRole))


class ExerciseModel(db_engine.Model):
    __tablename__ = config.EXERCISE_TABLE
    exercise_id = db_engine.Column(db_engine.Integer, primary_key=True)
    exercise_title = db_engine.Column(db_engine.String, unique=True)
    exercise_description = db_engine.Column(db_engine.String)
    exercise_type = db_engine.Column(db_engine.Enum(config.ExerciseType))
    exercise_content = db_engine.Column(db_engine.Text)
    exercise_solution = db_engine.Column(db_engine.Text)
    exercise_language = db_engine.Column(db_engine.Enum(config.ExerciseLanguage))


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
