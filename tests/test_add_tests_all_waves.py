from app.models.task import Task
from app.models.goal import Goal
import pytest
import unittest
from unittest.mock import Mock, patch
from app import db

# This fixture gets called in every test that
# references "one_task"
# This fixture creates a task and saves it in the database
# @pytest.fixture
# def one_task_no_mark_complete(app):
#     new_task = Task(
#         title="Go on my daily walk 🏞", description="Notice something new every day", completed_at=None)
#     db.session.add(new_task)
#     db.session.commit()


def test_get_tasks_with_invalid_query_param_returns_400(client, three_tasks):
    response = client.get("/tasks?sort=nope")
    response_body = response.get_json()

    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body["details"] == "Invalid data"
    tasks = Task.query.all()
    assert len(tasks) == 3 # no changes to three_tasks
    

def test_mark_complete_with_invalid_completed_at_returns_400(client):
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": "this isn't a date"
    })

    response_body = response.get_json()

    assert response.status_code == 400
    assert "task" not in response_body
    assert response_body["details"] == "Invalid date data"
    tasks = Task.query.all()
    assert len(tasks) == 0