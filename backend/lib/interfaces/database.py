#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask_sqlalchemy

from backend.lib.core import errors

db_engine = flask_sqlalchemy.SQLAlchemy()


class UserModel(db_engine.Model):
    # __tablename__ = "users"
    user_id = db_engine.Column(db_engine.Integer, primary_key=True)
    user_name = db_engine.Column(db_engine.String(100))
    user_cred = db_engine.Column(db_engine.String(32))


class ExerciseModel(db_engine.Model):
    # __tablename__ = "exercises"
    exercise_id = db_engine.Column(db_engine.Integer, primary_key=True)
    exercise_title = db_engine.Column(db_engine.String(100))


# class CourseModel(db_engine.Model):
#     pass
