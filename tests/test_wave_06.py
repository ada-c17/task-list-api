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


def test_post_tasks_to_goal_with_missing_task_ids(client, one_goal, three_tasks):
    response = client.post("/goals/1/tasks", json={})
    response_body = response.get_json()
    assert response.status_code == 400
    assert response_body["details"] == "Invalid data"

def test_post_tasks_to_goal_with_empty_task_ids(client, one_goal, three_tasks):
    response = client.post("/goals/1/tasks", json={
        "task_ids": []
        })
    response_body = response.get_json()
    assert response.status_code == 200
    assert "id" in response_body
    assert "task_ids" in response_body
    assert response_body == {
        "id": 1,
        "task_ids": []
    }

def test_post_tasks_to_goal_with_task_id_not_found(client, one_goal, three_tasks):
    response = client.post("/goals/1/tasks", json={
        "task_ids": [1, 2, 10]
        })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["message"] == "Task 10 not found."

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
    assert response_body["message"] == "Goal 1 not found."


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


def test_update_task_with_goal_id(client, one_task, one_goal):
    response = client.put("/tasks/1", json={
        "goal_id": 1
    })
    response_body = response.get_json()
    assert response.status_code == 200
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False,
            "goal_id": 1
        }
    }

def test_get_goals_sorted_asc(client, three_goals):
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"},
        {
            "id": 3,
            "title": "Eat healthy."},
        {
            "id": 2,
            "title": "Read more. Read often."}
    ]



def test_get_goals_sorted_desc(client, three_goals):
    response = client.get("/goals?sort=desc")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Read more. Read often."},
        {
            "id": 3,
            "title": "Eat healthy."},
        {
            "id": 1,
            "title": "Build a habit of going outside daily"}
    ]
