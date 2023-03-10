# kev.in

![image](https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00)
![image](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![image](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/License-GPL%20v3-yellow.svg?style=for-the-badge)

---

## Documentation

The documentation can be found [here](https://mlinke-ai.github.io/kev_in).


## Installation

Basically Kev.in can run on any system. It relies mostly on Python, some Python libraries (Flask and SQLAlchemy) and Docker.

### Dependencies

The necessary packages should be easily available on any recent system. Installation of the dependencies is not part of this documentation. Older versions of these packages may work but have not been tested.

- python == 3.10 or higher
- npm == 8.3

### Download

The source code of Kev.in can be downloaded from GitHub:

```
git clone https://github.com/mlinke-ai/kev_in.git
```

### Python packages

After cloning the repository, run

```
pip install -r requirements.txt
```

in the root folder.

### Frontend

The frontend is based on the Svelte framework which basically compiles static files at build time. To build the frontend change into the `frontend` folder and run

```
npm install
```

followed by

```
npm run build
```

### Executing

To run the server go back to the root folder an run:
```
python run.py --host --testing --clean
```
A Flask-server now will be live on the systems IP-address.