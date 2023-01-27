#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timezone

from flask import Response, current_app
from flask_jwt_extended import (create_access_token, get_jwt, get_jwt_identity,
                                set_access_cookies)


def user_id_from_cookie():
    pass


def is_admin_from_cookie():
    pass


def refresh_token(response: Response) -> Response:
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + current_app.config["JWT_REFRESH_PERIOD"])
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
    except (RuntimeError, KeyError):
        return response
    else:
        return response
