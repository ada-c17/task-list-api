from app.models.task import Task
import pytest


# 
def test_incorrect_args_for_sort_query(client):
    # Act
    response = client.get("/tasks?sort=nope")
    response_body = response.get_json()
    # Assert
    assert response_body == {"details":"Our sort selection is limited to: asc and desc"}

# def test_create_task_with_invalid_completed_at(client, ):
#     # Act
#     response = client.post("/tasks", json={
#         "title": "A Brand New Task",
#         "description": "Test Description",
#         "completed_at": "???"
#     })
#     response_body = response.get_json()
#     # Assert
#     assert response_body == "Incorrect date format, should be YYYY-MM-DD"
