#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
from datetime import timedelta

from flask_compress import Compress


class BaseConfig(object):
    # execution mode
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "5ebe0d2d-8079-4fe9-9a13-718a31be0cfd"
    # logging config
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = "kev_in.log"
    LOGGING_LEVEL = logging.DEBUG
    # security configuration
    SECURITY_PASSWORD_SALT = "eeGun1iupee2izou7ahw9fah"
    # caching configuration
    CACHE_TYPE = "simple"
    # compression config
    COMPRESS_MIMETYPES = [
        "text/html",
        "text/css",
        "text/xml",
        "application/json",
        "application/javascript",
    ]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    # JWT configuration
    JWT_COOKIE_SECURE = False
    JWT_CSRF_IN_COOKIES = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_SECRET_KEY = "3bc507e0-2966-4a2c-a89b-24ce8a16ab1e"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_PERIOD = timedelta(minutes=30)
    # miscellaneous configurations
    MAX_ITEMS_RETURNED = 20


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///kev_in.db"
    SECRET_KEY = "82a18580-b568-4813-958e-420c1facf963"


class StagingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    ENV = "staging"
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    SECRET_KEY = "942c3677-28ff-4841-bbd6-04f15b9d5a00"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    ENV = "prod"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SECRET_KEY = "4ec3ec4f-2657-4eac-b35c-ce96cfebc55c"


config = dict(
    dev="backend.config.DevelopmentConfig",
    staging="backend.config.StagingConfig",
    prod="backend.config.ProductionConfig",
    default="backend.config.DevelopmentConfig",
)


def configure_app(app, test_config=dict()):
    config_name = os.getenv("FLASK_CONFIGURATION", "default")
    app.config.from_object(config[config_name])
    app.config.from_pyfile("config.cfg", silent=True)
    app.config.from_mapping(test_config)
    # configure logging
    handler = logging.FileHandler(app.config["LOGGING_LOCATION"])
    handler.setLevel(app.config["LOGGING_LEVEL"])
    formatter = logging.Formatter(app.config["LOGGING_FORMAT"])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    # configure compression
    Compress(app)
