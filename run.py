#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from backend.server import Server


def main():
    parser = argparse.ArgumentParser(
        prog="Kev.in Management Script", description="The control script to manage the server."
    )
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    server = Server()
    server.run(args.debug)


if __name__ == "__main__":
    main()
