#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import shutil

from backend.server import Server


def main():
    parser = argparse.ArgumentParser(
        prog="Kev.in Management Script", description="The control script to manage the server."
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Run the flask server in debug mode")
    parser.add_argument(
        "-c", "--clean", action="store_true", help="Remove local database files before starting flask server"
    )
    parser.add_argument(
        "--host", action="store_true", help="Bind the flask server to the machines Ip address not 'localhost'"
    )
    args = parser.parse_args()

    if args.clean:
        shutil.rmtree("instance")

    server = Server()
    server.run(args.debug, args.host)


if __name__ == "__main__":
    main()
