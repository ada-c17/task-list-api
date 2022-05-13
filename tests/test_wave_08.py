# added tests for 100% Code Coverage
from app.models.task import Task
import pytest

def test_update_task_id_not_int(client):
    # Act
    response = client.get("/tasks/hello")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert len(response_body) == 1

def test_update_goal_id_not_int(client):
    # Act
    response = client.get("/goals/hello")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert len(response_body) == 1
