# Wave 3: Creating Custom Endpoints

## Goal

Our task list API allows users to meaningfully use the task resource. Users want to be able to mark a task as "complete" or "incomplete."

We want to design our API so that it stores a task's `completed_at` date as a datetime value in our database. In this scenario, our API does _not_ give users the `completed_at` date... it only gives the information if `is_complete` is `true` or `false`.

A task's `is_complete` is `true` when there is a datetime for the task's `completed_at` value. A task's `is_complete` is `false` when there is a `null`/`None` value for the tasks's `completed_at` value.

## Requirements

The following are required routes for wave 3. Feel free to implement the routes in any order within this wave.

### Tips

- Use the tests in `tests/test_wave_3.py` to guide your implementation.
- You may feel that there are missing tests and missing edge cases considered in this wave. This is intentional.
  - You have fulfilled wave 3 requirements if all of the wave 3 tests pass.
  - You are free to add additional features, as long as the wave 3 tests still pass. However, we recommend that you consider the future waves, first.
- A test uses a fixture named `completed_task` that is defined in `tests/conftest.py`. This fixture saves a task with a datetime value in `completed_at` to the test database.
- JSON's value of `true` is similar to Python's value of `True`, and `false` is similar to Python's `False`.
- SQL's value of `null` is similar to Python's value of `None`.
- Python has a [datetime library](https://docs.python.org/3/library/datetime.html#module-datetime) which we recommend using to represent dates in model attributes.

<!-- ### Mark Complete on an Incompleted Task

Given a task that has:

- An id `1`
- A `completed_at` attribute with a `null` value

when I send a `PATCH` request to `/tasks/1/mark_complete`,

then the task is updated, so that its `completed_at` value is the current date, and I get this response:

`200 OK`

```json
{
  "task": {
    "id": 1,
    "title": "Go on my daily walk 🏞",
    "description": "Notice something new every day",
    "is_complete": true
  }
}
``` -->

<!-- ### Mark Incomplete on a Completed Task

Given a task that has:

- An id `1`
- A `completed_at` attribute with a datetime value

when I send a `PATCH` request to `/tasks/1/mark_incomplete`,

then the task is updated, so that its `completed_at` value is `null`/`None`, and I get this response:

`200 OK`

```json
{
  "task": {
    "id": 1,
    "title": "Go on my daily walk 🏞",
    "description": "Notice something new every day",
    "is_complete": false
  }
}
``` -->

<!-- ### Mark Complete on a Completed Task

Given a task that has:

- An id `1`
- A `completed_at` attribute with a datetime value

when I send a `PATCH` request to `/tasks/1/mark_complete`,

then I want this to behave exactly like `/tasks/1/mark_complete` for an incomplete task. The task is updated, so that its `completed_at` value is the current date, and I get this response:

`200 OK`

```json
{
  "task": {
    "id": 1,
    "title": "Go on my daily walk 🏞",
    "description": "Notice something new every day",
    "is_complete": true
  }
}
``` -->

<!-- ### Mark Incomplete on an Incompleted Task

Given a task that has:

- An id `1`
- A `completed_at` attribute with a `null` value

when I send a `PATCH` request to `/tasks/1/mark_incomplete`,

then I want this to behave exactly like `/tasks/1/mark_incomplete` for a complete task. Its `completed_at` value remains as `null`/`None`, and I get this response:

`200 OK`

```json
{
  "task": {
    "id": 1,
    "title": "Go on my daily walk 🏞",
    "description": "Notice something new every day",
    "is_complete": false
  }
}
``` -->

## Mark Complete and Mark Incomplete for Missing Tasks

Given that there are no tasks with the ID `1`,

When I send a `PATCH` request to `/tasks/1/mark_complete` or a `PATCH` request to `/tasks/1/mark_incomplete`,

Then I get a `404 Not Found`.

You may choose the response body.

Make sure to complete the tests for non-existing tasks to check that the correct response body is returned.
