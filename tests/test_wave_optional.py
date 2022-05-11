from app.models.task import Task
import pytest


# 
def test_incorrect_args_for_sort_query(client):
    # Act
    response = client.get("/tasks?sort=nope")
    response_body = response.get_json()
    # Assert
    assert response_body == {"details":"Our sort selection is limited to: asc and desc"}
