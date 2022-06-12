# Setup

## Goal

The goal for setup is to cover all of the set up needed at the beginning of this project, which includes:

1. Forking and cloning
1. Managing dependencies
1. Setting up development and test databases
1. Setting up a `.env` file
1. Running `$ flask db init`
1. Running `$ flask run` and `$ FLASK_ENV=development flask run`

# Requirements

## Fork and Clone

1. Fork this project repo to your own personal account
1. Clone this new forked project

## Managing Dependencies

Create a virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ # You're in activated virtual environment!
```

Install dependencies (we've already gathered them all into a `requirements.txt` file):

```bash
(venv) $ pip install -r requirements.txt
```

## Setting Up Development and Test Databases

Create two databases:

1. A development database named `task_list_api_development`
1. A test database named `task_list_api_test`

## Creating a `.env` File

Create a file named `.env`.

Create two environment variables that will hold your database URLs.

1. `SQLALCHEMY_DATABASE_URI` to hold the path to your development database
1. `SQLALCHEMY_TEST_DATABASE_URI` to hold the path to your development database

Your `.env` may look like this:

```
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/task_list_api_development
SQLALCHEMY_TEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/task_list_api_test
```

## Run `$ flask db init`

Run `$ flask db init`.

**_After you make your first model in Wave 1_**, run the other commands `migrate` with -m to add message so we know what were talking about and `upgrade`.

## Run `$ flask run` or `$ FLASK_ENV=development flask run`

Check that your Flask server can run with `$ flask run`.

We can run the Flask server specifying that we're working in the development environment. This enables hot-reloading, which is a feature that refreshes the Flask server every time there is a detected change.

```bash
$ FLASK_ENV=development flask run
```

**It is highly recommended to run the Flask servers with this command**.
