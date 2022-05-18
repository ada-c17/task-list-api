import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.models.task import Task
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_on_incomplete_task(client, one_task):
    # Arrange
    """
    The future Wave 4 adds special functionality to this route,
    so for this test, we need to set-up "mocking."

    Mocking will help our tests work in isolation, which is a
    good thing!

    We need to mock any POST requests that may occur during this
    test (due to Wave 4).

    There is no action needed here, the tests should work as-is.
    """
    with patch("requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        # Act
        response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body["task"]["is_complete"] == True
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": True
        }
    }
    assert Task.query.get(1).completed_at


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_incomplete_on_complete_task(client, completed_task):
    # Act
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["task"]["is_complete"] == False
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }
    assert Task.query.get(1).completed_at == None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_on_completed_task(client, completed_task):
    # Arrange
    """
    The future Wave 4 adds special functionality to this route,
    so for this test, we need to set-up "mocking."

    Mocking will help our tests work in isolation, which is a
    good thing!

    We need to mock any POST requests that may occur during this
    test (due to Wave 4).

    There is no action needed here, the tests should work as-is.
    """
    with patch("requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        # Act
        response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body["task"]["is_complete"] == True
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": True
        }
    }
    assert Task.query.get(1).completed_at


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_incomplete_on_incomplete_task(client, one_task):
    # Act
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["task"]["is_complete"] == False
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }
    assert Task.query.get(1).completed_at == None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_missing_task(client):
    # Act
    response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************
    assert response_body == {"message": "task 1 not found"}


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_incomplete_missing_task(client):
    # Act
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************
    assert response_body == {"message": "task 1 not found"}


# Let's add this test for creating tasks, now that
# the completion functionality has been implemented
# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_with_valid_completed_at(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": datetime.utcnow()
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": True
        }
    }
    new_task = Task.query.get(1)
    assert new_task
    assert new_task.title == "A Brand New Task"
    assert new_task.description == "Test Description"
    assert new_task.completed_at


# Let's add this test for updating tasks, now that
# the completion functionality has been implemented
# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task_with_completed_at_date(client, completed_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
        "completed_at": datetime.utcnow()
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": True
        }
    }
    task = Task.query.get(1)
    assert task.title == "Updated Task Title"
    assert task.description == "Updated Test Description"
    assert task.completed_at
