from app.models.task import Task
import pytest

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_invalid_task(client):
    # Act
    response = client.get("/tasks/hello")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid id hello"}
    assert len(response_body) == 1

def test_invalid_goal(client):
    # Act
    response = client.get("/goals/work")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Invalid id work"}
    assert len(response_body) == 1