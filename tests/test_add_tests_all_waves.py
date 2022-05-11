from app.models.task import Task
from app.models.goal import Goal
import pytest

def test_get_tasks_with_invalid_query_param_returns_400(client, three_tasks):
    response = client.get("/tasks?sort=nope")
    response_body = response.get_json()

    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body["details"] == "Invalid data"
