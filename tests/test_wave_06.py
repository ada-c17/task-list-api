from app.models.goal import Goal
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_post_task_ids_to_goal(client, one_goal, three_tasks):
    # Act
    response = client.post("/goals/1/tasks", json={
        "task_ids": [1, 2, 3]
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "id" in response_body
    assert "task_ids" in response_body
    assert response_body == {
        "id": 1,
        "task_ids": [1, 2, 3]
    }

    # Check that Goal was updated in the db
    assert len(Goal.query.get(1).tasks) == 3


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_post_task_ids_to_goal_already_with_goals(client, one_task_belongs_to_one_goal, three_tasks):
    # Act
    response = client.post("/goals/1/tasks", json={
        "task_ids": [1, 4]
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "id" in response_body
    assert "task_ids" in response_body
    assert response_body == {
        "id": 1,
        "task_ids": [1, 4]
    }
    assert len(Goal.query.get(1).tasks) == 2


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_for_specific_goal_no_goal(client):
    # Act
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************
    assert response_body == {"details": "No model data with id: 1"}


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_for_specific_goal_no_tasks(client, one_goal):
    # Act
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "tasks" in response_body
    assert len(response_body["tasks"]) == 0
    assert response_body == {
        "id": 1,
        "title": "Build a habit of going outside daily",
        "tasks": []
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_for_specific_goal(client, one_task_belongs_to_one_goal):
    # Act
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "tasks" in response_body
    assert len(response_body["tasks"]) == 1
    assert response_body == {
        "id": 1,
        "title": "Build a habit of going outside daily",
        "tasks": [
            {
                "id": 1,
                "goal_id": 1,
                "title": "Go on my daily walk 🏞",
                "description": "Notice something new every day",
                "is_complete": False
            }
        ]
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task_includes_goal_id(client, one_task_belongs_to_one_goal):
    response = client.get("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "task" in response_body
    assert "goal_id" in response_body["task"]
    assert response_body == {
        "task": {
            "id": 1,
            "goal_id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }

# Additional tests that I added

def test_add_task_to_goal_returns_error_if_missing_task_ids_field(client):
    response = client.post("goals/1/tasks", json={})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "task_ids field required in request"}


def test_invalid_key_for_updating_task(client, one_task):
    response = client.put("/tasks/1", json={
        "titl": "Walk 2 miles every day",
        "description": "Exercising habits",
    })

    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {'details': "Missing key: 'title'"}


def test_invalid_id_for_getting_task(client, one_task):
    response = client.get("/tasks/foo")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {'details': "Invalid id: foo"}