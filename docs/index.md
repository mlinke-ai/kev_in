---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2022-11-26
---

# Documentation for Kev.in

Kev.in is a learning platform for programming beginners. It is released under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html).

The source code of Kev.in can be downloaded at:

[GitHub](https://github.com/mlinke-ai/kev_in)

The documentation can be found online at:

[GitHub Pages](https://mlinke-ai.github.io/kev_in/)

Bug reports should be done through the [Issue Tracker](https://github.com/mlinke-ai/kev_in/issues) of Kev.in on GitHub.

# Testing

To perform tests, start the server in testing mode with `python3 run.py --debug --clean --testing` and run `python3 -m unittest discover` in the root of the project.

# Coverage

The test coverage can be tested with `python3 -m coverage run -m unittest` and `python3 -m coverage report -i`.
