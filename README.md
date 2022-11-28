![GitHub tag (latest SemVer)](https://carlos-shields-io.herokuapp.com/github/v/tag/mextalki/mextalki)
![GitHub](https://carlos-shields-io.herokuapp.com/github/license/mextalki/mextalki)
![GitHub Pipenv locked Python version](https://carlos-shields-io.herokuapp.com/github/pipenv/locked/python-version/mextalki/mextalki)
![GitHub Pipenv locked dependency version](https://carlos-shields-io.herokuapp.com/github/pipenv/locked/dependency-version/mextalki/mextalki/django)
![GitHub branch checks state](https://carlos-shields-io.herokuapp.com/github/checks-status/mextalki/mextalki/master)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

# Mextalki Site
Mextalki [site](https://www.mextalki.com) source code.


## Requirements
- [Python 3.7](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv)


## Installation
1. Create env File
```sh
cp .env.example .env
```
2. Install Dependencies with pipenv
```sh
pipenv install --dev
```

## Run Project
Run project:
```sh
make run
```

## Format & Lint
To format code:
```sh
make format
```

To check lint issues:
```sh
make lint
```

## Django Migrations
Check migrations:
```sh
make show_migrations
```

Create new migrations:
```sh
make make_migrations
```

Migrate new migrations:
```sh
make migrate
```