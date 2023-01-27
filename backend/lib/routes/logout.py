#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Response, redirect
from flask_restful import Resource

class LogoutResource(Resource):

    def post(self) -> Response:

        response = redirect("/")
        response.set_cookie("token", max_age=0)

        return response
