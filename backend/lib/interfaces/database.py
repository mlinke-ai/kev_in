#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask_sqlalchemy

from backend.lib.core import errors, config

db_engine = flask_sqlalchemy.SQLAlchemy()


class UserModel(db_engine.Model):
    __tablename__ = config.USER_TABLE
    user_id = db_engine.Column(db_engine.Integer, primary_key=True)
    user_name = db_engine.Column(db_engine.String(100))
    user_pass = db_engine.Column(db_engine.String(64))


class ExerciseModel(db_engine.Model):
    __tablename__ = config.EXERCISE_TABLE
    exercise_id = db_engine.Column(db_engine.Integer, primary_key=True)
    exercise_title = db_engine.Column(db_engine.String(100))


# class CourseModel(db_engine.Model):
#     pass
