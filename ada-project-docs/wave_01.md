# Wave 1: CRUD for One Model

## Goal

Our task list API should be able to work with an entity called `Task`.

Tasks are entities that describe a task a user wants to complete. They contain a:

- title to name the task
- description to hold details about the task
- an optional datetime that the task is completed on

Our goal for this wave is to be able to create, read, update, and delete different tasks. We will create RESTful routes for this different operations.

# Requirements

## Task Model

There should be a `Task` model that lives in `app/models/task.py`.

Tasks should contain these attributes. Feel free to change the name of the `task_id` column if you would like. **The tests require the remaining columns to be named exactly** as `title`, `description`, and `completed_at`.

- `task_id`: a primary key for each task
- `title`: text to name the task
- `description`: text to describe the task
- `completed_at`: a datetime that has the date that a task is completed on. **Can be _nullable_,** and contain a null value. A task with a `null` value for `completed_at` has not been completed. When we create a new task, `completed_at` should be `null` AKA `None` in Python.

### Tips

- SQLAlchemy's column type for text is `db.String`. The column type for datetime is `db.DateTime`.
- SQLAlchemy supports _nullable_ columns with specific syntax.
- Don't forget to run:
  - `flask db init` once during setup
  - `flask db migrate` every time there's a change in models, in order to generate migrations
  - `flask db upgrade` to run all generated migrations
- We can assume that the value of each task's `completed_at` attribute will be `None`, until wave 3. (Read below for examples)
- We can assume that the API will designate `is_complete` as `false`, until wave 3. (Read below for examples)

## CRUD for Tasks

The following are required routes for wave 1. Feel free to implement the routes in any order within this wave.

### Tips

- Pay attention to the exact shape of the expected JSON. Double-check nested data structures and the names of the keys for any mispellings.
  - That said, remember that dictionaries do not have an implied order. This is still true in JSON with objects. When you make Postman requests, the order of the key/value pairings within the response JSON object does not need to match the order specified in this document. (The term "object" in JSON is analagous to "dictionary" in Python.)
- Use the tests in `tests/test_wave_01.py` to guide your implementation.
- You may feel that there are missing tests and missing edge cases considered in this wave. This is intentional.
  - You have fulfilled wave 1 requirements if all of the wave 1 tests pass.
  - You are free to add additional features, as long as the wave 1 tests still pass. However, we recommend that you consider the future waves, first.
- Some tests use a fixture named `one_task` that is defined in `tests/conftest.py`. This fixture saves a specific task to the test database.

### CLI

In addition to testing your code with pytest and postman, you can play test your code with the CLI (Command Line Interface) by running `python3 cli/main.py`. The flask server needs to be running to run the CLI.

### Create a Task: Valid Task With `null` `completed_at`

As a client, I want to be able to make a `POST` request to `/tasks` with the following HTTP request body

```json
{
  "title": "A Brand New Task",
  "description": "Test Description",
}
```

and get this response:

`201 CREATED`

```json
{
  "task": {
    "id": 1,
    "title": "A Brand New Task",
    "description": "Test Description",
    "is_complete": false
  }
}
```

so that I know I successfully created a Task that is saved in the database.

### Get Tasks: Getting Saved Tasks

As a client, I want to be able to make a `GET` request to `/tasks` when there is at least one saved task and get this response:

`200 OK`

```json
[
  {
    "id": 1,
    "title": "Example Task Title 1",
    "description": "Example Task Description 1",
    "is_complete": false
  },
  {
    "id": 2,
    "title": "Example Task Title 2",
    "description": "Example Task Description 2",
    "is_complete": false
  }
]
```

### Get Tasks: No Saved Tasks

As a client, I want to be able to make a `GET` request to `/tasks` when there are zero saved tasks and get this response:

`200 OK`

```json
[]
```

### Get One Task: One Saved Task

As a client, I want to be able to make a `GET` request to `/tasks/1` when there is at least one saved task and get this response:

`200 OK`

```json
{
  "task": {
    "id": 1,
    "title": "Example Task Title 1",
    "description": "Example Task Description 1",
    "is_complete": false
  }
}
```

### Update Task

As a client, I want to be able to make a `PUT` request to `/tasks/1` when there is at least one saved task with this request body:

```json
{
  "title": "Updated Task Title",
  "description": "Updated Test Description",
}
```

and get this response:

`200 OK`

```json
{
  "task": {
    "id": 1,
    "title": "Updated Task Title",
    "description": "Updated Test Description",
    "is_complete": false
  }
}
```

Note that the update endpoint does update the `completed_at` attribute. This will be updated with custom endpoints implemented in Wave 03.

### Delete Task: Deleting a Task

As a client, I want to be able to make a `DELETE` request to `/tasks/1` when there is at least one saved task and get this response:

`200 OK`

```json
{
  "details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
}
```

### No matching Task: Get, Update, and Delete

As a client, if I make any of the following requests:

  * `GET` `/tasks/<task_id>`
  * `UPDATE` `/tasks/<task_id>`
  * `DELETE` `/tasks/<task_id>`

and there is no existing task with `task_id`

The response code should be `404`.

You may choose the response body.

Make sure to complete the tests for non-existing tasks to check that the correct response body is returned.
 

### Create a Task: Invalid Task With Missing Data

#### Missing `title`

As a client, I want to be able to make a `POST` request to `/tasks` with the following HTTP request body

```json
{
  "description": "Test Description",
}
```

and get this response:

`400 Bad Request`

```json
{
  "details": "Invalid data"
}
```

so that I know I did not create a Task that is saved in the database.

#### Missing `description`

If the HTTP request is missing `description`, we should also get this response:

`400 Bad Request`

```json
{
  "details": "Invalid data"
}
```
