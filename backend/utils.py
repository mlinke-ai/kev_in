#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime, timezone

from flask import Response, current_app
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies

from backend.database.models import BlocklistModel, db


def user_id_from_token():
    pass


def user_id_from_token():
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


def revoked_token_check(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    query = db.select(BlocklistModel).filter_by(blocklist_jti=jti)
    token = db.session.execute(query).scalar()
    return token is not None


def get_url(url: str, **kwargs: dict) -> str:
    for key, value in kwargs.items():
        if re.search(key, url) == None:
            url += f"&{key}={value}"
        else:
            url = re.sub(f"(?<={key}=)[^&]+(?=&|$)", str(value), url)
    return url
