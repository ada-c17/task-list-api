from app.models.task import Task
import pytest


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task_invalid_id_is_bad_request(client):
    # Act
    response = client.get("/tasks/invalid_id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body == {"message":f"Task id 'invalid_id' is invalid"}

def test_update_task_invalid_id_is_bad_request(client):
    # Act
    response = client.put("/tasks/invalid_id", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body == {"message":f"Task id 'invalid_id' is invalid"}