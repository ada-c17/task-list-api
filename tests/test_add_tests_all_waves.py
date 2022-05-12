from http.client import responses
from app.models.task import Task
from app.models.goal import Goal
import pytest
from app import db
from datetime import datetime



# Helper functions
# would we want to write tests to check that validate_task and validate_goal 
# are working correctly?


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

# datetime format 1: 'Sat, 07 May 2022 23:59:31 GMT'
def test_create_tasks_takes_one_datetime_for_completed_at(client):
    response = client.post("/tasks", json={
        "title": "New task",
        "description": "Description for new task",
        "completed_at": 'Sat, 07 May 2022 23:59:31 GMT'
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "task" in response_body
    assert response_body["task"] == {
        "id": 1,
        "title": "New task",
        "description": "Description for new task",
        "is_complete": True
    }
    new_task = Task.query.get(1)
    assert new_task
    assert new_task.title == "New task"
    assert new_task.description == "Description for new task"
    assert new_task.completed_at == datetime.strptime('Sat, 07 May 2022 23:59:31 GMT', 
                    '%a, %d %B %Y %H:%M:%S %Z')

# datetime format 2: '2022-05-07 18:48:06.598253'
def test_create_tasks_takes_second_datetime_for_completed_at(client):
    response = client.post("/tasks", json={
        "title": "New task",
        "description": "Description for new task",
        "completed_at": '2022-05-07 18:48:06.598253'
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "task" in response_body
    assert response_body["task"] == {
        "id": 1,
        "title": "New task",
        "description": "Description for new task",
        "is_complete": True
    }
    new_task = Task.query.get(1)
    assert new_task
    assert new_task.title == "New task"
    assert new_task.description == "Description for new task"
    assert new_task.completed_at == datetime.strptime('2022-05-07 18:48:06.598253', 
                    '%Y-%m-%d %H:%M:%S.%f')

def test_create_task_with_invalid_completed_at_returns_400(client):
    response = client.post("/tasks", json={
        "title": "New task",
        "description": "Description for new task",
        "completed_at": "Not a datetime"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["details"] == "Invalid date data"
    tasks = Task.query.all()
    assert len(tasks) == 0

# WAVE 2
def test_get_tasks_with_invalid_query_param_returns_400(client, three_tasks):
    response = client.get("/tasks?sort=nope")
    response_body = response.get_json()

    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body["details"] == "Invalid data"

# WAVE 5
def test_update_goal_with_no_title_returns_400(client, one_goal):
    response = client.put("goals/1")
    response_body = response.get_json()

    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body["details"] == "Goal needs a title"
    goal = Goal.query.get(1)
    assert goal.title == "Build a habit of going outside daily"


# WAVE 6 (and validate_task)
def test_invalid_task_id_list_returns_400(client, one_goal):
    response = client.post("/goals/1/tasks", json={"task_ids": ["one", "two"]})
    response_body = response.get_json()

    assert response.status_code == 400
    assert "id" not in response_body
    assert "task_ids" not in response_body
    assert response_body["details"] == "one is not valid input."