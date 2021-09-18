<p align="center" style="font-size: 10rem">RALPH</p>


![main](https://github.com/fmp95/ralph/actions/workflows/main.yml/badge.svg) ![development](https://github.com/fmp95/ralph/actions/workflows/development.yml/badge.svg)


<hr>

# About
Ralph is an API built using Django Ninja. It should be packed with basic features that online catalogues would need to display their products online. _The front-end project will come next, once the API is mostly done and the repository will be linked here_.

# Dependencies
- Python 3.9.
- Django Ninja.
- Bcrypt.
- Python-jose.
- Any other listed in [requirements](requirements).

# How to run
This project comes with a handy [makefile](makefile) that has some easy to run commands that should help setting all you need to run the API:

| Command             | Description                                                            |
| ------------------- | ---------------------------------------------------------------------- |
| `make setup-dev`    | Creates a python virtual env and install all development dependencies. |
| `make setup-django` | Make database migrations and setup django.                             |
| `make run`          | Run API in a local server.                                             |

# Features
Even though Ralph uses lots of features that comes from Django, some were implemented in a different way (for study purpose or customization). They are:
- Authentication using Bearer tokens.
- Authentication levels divided in roles and individual permissions.
- Database tables modeling.
- User registering.

# Notes
This repository is mainly for study purpose. Things are subject to change at any time and not be at the most correct form of application. Feel free to leave suggestions.