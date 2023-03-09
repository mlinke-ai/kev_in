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

import argparse
import shutil

from backend.lib.core import config
from backend.server import Server


def main():
    parser = argparse.ArgumentParser(
        prog="Kev.in Management Script",
        description="The control script to manage the server.",
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Run the flask server in debug mode")
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Remove local database files before starting flask server",
    )
    parser.add_argument(
        "-t",
        "--testing",
        action="store_true",
        help="Starts the server in test mode. Overrules environment variables.",
    )
    parser.add_argument(
        "--host",
        action="store_true",
        help="Bind the flask server to the machines Ip address not 'localhost'",
    )
    args = parser.parse_args()

    if args.clean:
        shutil.rmtree("instance", ignore_errors=True)
    if args.testing:
        database_uri = config.TESTING_DATABASE_URI
    else:
        database_uri = config.DATABASE_URI

    server = Server(database_uri)
    server.run(args.debug, args.host)


if __name__ == "__main__":
    main()
