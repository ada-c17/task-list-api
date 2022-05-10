# Wave 2: Using Query Params

## Goal

Our task list API allows users to create tasks and get a list of all tasks. Our users will find it useful to be able to sort through these tasks by title! Our goal is to implement a basic sorting feature for our tasks.

## Requirements

The following are required routes for wave 2. Feel free to implement the routes in any order within this wave.

### Tips

- Pay attention to the exact shape of the expected JSON. Double-check nested data structures and the names of the keys for any mispellings.
- Use the tests in `tests/test_wave_02.py` to guide your implementation.
- You may feel that there are missing tests and missing edge cases considered in this wave. This is intentional.
  - You have fulfilled wave 2 requirements if all of the wave 2 tests pass.
  - You are free to add additional features, as long as the wave 2 tests still pass. However, we recommend that you consider the future waves, first.
- Some tests use a fixture named `three_tasks` that is defined in `tests/conftest.py`. This fixture saves three different tasks with three different titles to the test database.

### Sorting Tasks: By Title, Ascending

As a client, I want to be able to make a `GET` request to `/tasks?sort=asc` when there is more than one saved task, and get an array of tasks sorted by **title**. The titles should be in _ascending_ order, where a task with the title "A" is sorted before a task with the title "B."

I want to get this response:

`200 OK`

```json
[
  {
    "id": 1,
    "title": "A",
    "description": "Example Task Description 1",
    "is_complete": false
  },
  {
    "id": 2,
    "title": "B",
    "description": "Example Task Description 2",
    "is_complete": false
  }
]
```

### Sorting Tasks: By Title, Descending

As a client, I want to be able to make a `GET` request to `/tasks?sort=desc` when there is more than one saved task, and get an array of tasks sorted by **title**. The titles should be in _descending_ order, where a task with the title "B" is sorted before a task with the title "A."

I want to get this response:

`200 OK`

```json
[
  {
    "id": 2,
    "title": "B",
    "description": "Example Task Description 2",
    "is_complete": false
  },
  {
    "id": 1,
    "title": "A",
    "description": "Example Task Description 1",
    "is_complete": false
  }
]
```

