---
title: Kev.in
summary: A learning platform for programming beginners.
authors:
    - Max Linke
    - and others
date: 2022-11-26
---

# Installation of Kev.in

Basically Kev.in can run on any system. It relies mostly on Python, some Python libraries (Flask and SQLAlchemy) and Docker.

## Dependencies

The necessary packages should be easily available on any recent system. Installation of the dependencies is not part of this documentation. Older versions of these packages may work but have not been tested.

- python == 3.10 or higher
- npm == 8.3

## Download

The source code of Kev.in can be downloaded from GitHub:

```
git clone https://github.com/mlinke-ai/kev_in.git
```

## Python packages

After cloning the repository, run

```
pip install -r requirements.txt
```

in the root folder.

## Frontend

The frontend is based on the Svelte framework which basically compiles static files at build time. To build the frontend change into the `frontend` folder and run

```
npm install
```

followed by

```
npm run build
```

## Executing

To run the server go back to the root folder an run:
```
python run.py --host --testing --clean
```
A Flask-server now will be live on the systems IP-address.

# Run as Docker container

TODO: add documentation