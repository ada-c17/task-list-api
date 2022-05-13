import pytest
from app.models.goal import Goal


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_one_saved_goal(client, one_goal):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal(client, one_goal):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    }


# @pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found_id_with_empty_db(client):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find goal with id 1"}
    assert Goal.query.all() == []

    # raise Exception("Complete test")


# create my test to update id with populated db id not found
def test_update_goal_not_found_id_with_populated_db(client, one_goal):
    # Act
    response = client.put("/goals/111", json={
        "title": "Updated Goal Title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find goal with id 111"}


# create my test to update id with populated db id is invalid
def test_update_goal_with_invalid_id_with_populated_db(client, one_goal):
    # Act
    response = client.put("/goals/my_goal", json={
        "title": "Updated Task Title"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "msg" in response_body
    assert response_body ==  {"msg": "Invalid id my_goal"}


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "My New Goal"
        }
    }


# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal(client, one_goal):
    # raise Exception("Complete test")
    # Act
    response = client.put("/goals/1", json={
        "title": "Change goal title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Change goal title"
        }
    }


# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    # raise Exception("Complete test")
    # Act
    response = client.put("/goals/456", json={
        "title": "Change goal title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find goal with id 456"}


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal(client, one_goal):
    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }
    assert Goal.query.get(1) == None

    # Check that the goal was deleted
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find goal with id 1"}

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


# @pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found_with_empty_db(client):
    # raise Exception("Complete test")

    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find goal with id 1"}
    assert Goal.query.all() == []


# create my test to delete id with populated db id not found
# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal_not_found_with_id_with_populated_db(client, one_goal):
    # Act
    response = client.delete("/goals/12121")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "msg" in response_body
    assert response_body ==  {"msg": "Could not find goal with id 12121"}


# create my test to delete id with populated db id is invalid
# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal_not_found_invalid_id_with_populated_db(client, one_goal):
    # Act
    response = client.delete("/goals/bad_goal")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "msg" in response_body
    assert response_body ==  {"msg": "Invalid id bad_goal"}


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
