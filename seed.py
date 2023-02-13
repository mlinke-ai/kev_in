#!/usr/bin/python3
# -*- coding: utf-8 -*-

from backend import app
from backend.database.models import ExerciseLanguage, ExerciseModel, ExerciseType, SolutionModel, UserModel, db


def create_sadmin(context):
    sadmin = UserModel("sadmin", "sadmin", "sadmin@example.com", 1)
    context.session.add(sadmin)
    context.session.commit()


def create_tuser(context):
    user = UserModel("tuser", "tuser", "tuser@example.com", 1)
    context.session.add(user)
    context.session.commit()


def create_exercises(context):
    for i in range(10):
        for t in list(ExerciseType):
            exercise = ExerciseModel(f"{t.name} {i}", f"Dummy {t.name} number {i}", t, {}, {}, ExerciseLanguage.Python)
            context.session.add(exercise)
    context.session.commit()


def create_solutions(context):
    solution = SolutionModel()
    context.session.add(solution)
    context.session.commit()


with app.app_context():
    db.drop_all()
    db.create_all()
    app.logger.info("Seeding database with SAdmin account")
    create_sadmin(db)
    app.logger.info("Seeding database with TUser account")
    create_tuser(db)
    app.logger.info("Seeding database with example exercises")
    create_exercises(db)
    app.logger.info("Seeding database with example solutions")
    # create_solutions(db)
