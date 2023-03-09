#!/usr/bin/python3
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

import re
from datetime import datetime, timezone

from flask import Response, current_app
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies

from backend.database.models import BlocklistModel, db


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
