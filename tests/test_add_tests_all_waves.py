from app.models.task import Task
from app.models.goal import Goal
import pytest
import unittest
from unittest.mock import Mock, patch
from app import db


# WAVE 1
def test_update_task_returns_400_with_no_title(client, one_task):
    response = client.put("/tasks/1", json={"description": "New task description"})
    response_body = response.get_json()

    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body["details"] == "Task needs both a title and description"
    task = Task.query.get(1)
    assert task.description == "Notice something new every day"

def test_update_task_returns_400_with_no_description(client, one_task):
    response = client.put("/tasks/1", json={"title": "New Title"})
    response_body = response.get_json()

    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body["details"] == "Task needs both a title and description"
    task = Task.query.get(1)
    assert task.title == "Go on my daily walk 🏞"

def test_update_goal_with_no_title_returns_400(client, one_goal):
    response = client.put("goals/1")
    response_body = response.get_json()

    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body["details"] == "Goal needs a title"
    goal = Goal.query.get(1)
    assert goal.title == "Build a habit of going outside daily"


# WAVE 2
def test_get_tasks_with_invalid_query_param_returns_400(client, three_tasks):
    response = client.get("/tasks?sort=nope")
    response_body = response.get_json()

    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body["details"] == "Invalid data"

# WAVE 1 and 3 (?)
# write tests to check that create_one_task adds in datetime if appropriate format
# 1: 'Sat, 07 May 2022 23:59:31 GMT'
# 2: '2022-05-07 18:48:06.598253'
# 3: else, invalid type is 400

# Helper functions
# would we want to write tests to check that validate_task and validate_goal 
# are working correctly?


# WAVE 6 (and validate_task)
def test_invalid_task_id_list_returns_400(client, one_goal):
    response = client.post("/goals/1/tasks", json={"task_ids": ["one", "two"]})
    response_body = response.get_json()

    assert response.status_code == 400
    assert "id" not in response_body
    assert "task_ids" not in response_body
    assert response_body["details"] == "one is not valid input."