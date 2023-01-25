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

# Download

The source code of Kev.in can be downloaded from GitHub:

```
git clone https://github.com/mlinke-ai/kev_in.git
```

# Installation

## Dependencies

The necessary packages should be easily available on any recent system. Installation of the dependencies is not part of this documentation. Older versions of these packages may work but have not been tested.

- python == 3.10 (but even down to version 3.6 should be fine)
- npm == 8.3

## Installation

### Python packages

After cloning the repository, run

```
pip install -r requirements.txt
```

in the root folder.

### Frontend

The frontend is based on the Svelte framework which basically compiles static files at build time. To build the frontend change into the `frontend` folger and run

```
npm install
```

followed by

```
npm run build
```

# Run as Docker container

TODO: add documentation
