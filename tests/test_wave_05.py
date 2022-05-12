from app.models.goal import Goal
import pytest


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


#@pytest.mark.skip(reason="No way to test this feature yet")
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


#@pytest.mark.skip(reason="No way to test this feature yet")
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


#@pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found(client):
    
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    #raise Exception("Complete test")
    # Assert
    # ---- Complete Test ----
    assert "details" in response_body
    assert response_body == {
        'details': f"Could not find goal"}
    # ---- Complete Test ----


#@pytest.mark.skip(reason="No way to test this feature yet")
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


#@pytest.mark.skip(reason="test to be completed by student")
def test_update_goal(client, one_goal):
    # Act
    # ---- Complete Act Here ----
    response = client.put("/goals/1", json={
        "title": "My updated Goal"
    })
    response_body = response.get_json()

    # Assert
    # ---- Complete Assertions Here ----
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "My updated Goal"}}
    goal = Goal.query.get(1)
    assert goal.title == "My updated Goal"
    assert goal.goal_id == 1
    # ---- Complete Assertions Here ---- 


#@pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"
    })
    response_body = response.get_json()

    # Assert
    # ---- Complete Assertions Here ----
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {
        'details': f"Could not find goal"}
    assert Goal.query.get(1) == None
    # ---- Complete Assertions Here ----


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal(client, one_goal):
    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()
    assert Goal.query.get(1) == None
    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }

    
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


#@pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found(client):
    # Check that the goal was deleted
    
    # Act
    # ---- Complete Act Here ----
    response = client.get("/goals/1")
    response_body = response.get_json()
    Goal.query.all() == [] 
    # Assert
    # ---- Complete Assertions Here ----
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {
        'details': f"Could not find goal"}
    # ---- Complete Assertions Here ----


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
