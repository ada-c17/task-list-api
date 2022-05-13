from app.models.goal import Goal
import pytest

# Test 32
#@pytest.mark.skip(reason="No way to test this feature yet")
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

# Test 33
#@pytest.mark.skip(reason="No way to test this feature yet")
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

# Test 34
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_for_specific_goal_no_goal(client):
    # Act
    response = client.get("/goals/1/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    #raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    assert len(response_body) == 1
    assert response_body 
    # *****************************************************************

# Test 35
#@pytest.mark.skip(reason="No way to test this feature yet")
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

# Test 36
#@pytest.mark.skip(reason="No way to test this feature yet")
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

# Test 37
#@pytest.mark.skip(reason="No way to test this feature yet")
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


### Extra Tests ###
# Test 38
#@pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_invalid(client):
    # Act
    response = client.get("/goals/hello")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body == {"message": "goal hello invalid"}
    

# Test 39
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task_invalid(client):
    # Act
    response = client.get("/tasks/hello")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert len(response_body) == 1
    assert response_body == {"message": "task hello invalid"}


# Test 40
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_filter_by_title(client, three_tasks):
    # Act
    response = client.get("/tasks?title=Water%20the%20garden%20🌷")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,  
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False
        }
    ]
# Test 41
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_by_id(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {  
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False},
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False}
    ]


# Test 42
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_sort_by_title(client, three_goals):
    # Act
    response = client.get("/goals?sort=title")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,  
            "title": "Drink more water"
        },
        {
            "id": 1,
            "title": "Exercise more"
        },
        {
            "id": 2,
            "title": "Learn to code"
        }
    ]

