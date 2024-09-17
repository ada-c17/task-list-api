import pytest
from app.models.goal import Goal


pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


pytest.mark.skip(reason="No way to test this feature yet")
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

pytest.mark.skip(reason="No way to test this feature yet")
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

pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal_with_invalid_id(client, one_goal):
    # Act
    response = client.get("/goals/hello")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {"details": "Invalid data"}

pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal_sorted_asc(client, three_goals):
    # Act
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"},
        {
            "id": 3,
            "title": "Call my parents often"},
        {
            "id": 2,
            "title": "Work out"
        },
    ]

pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal_sorted_desc(client, three_goals):
    # Act
    response = client.get("/goals?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Work out"},
        {
            "id": 3,
            "title": "Call my parents often"},
        {
            "id": 1,
            "title": "Build a habit of going outside daily"}
    ]

pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal_sorted_by_id(client, three_goals):
    # Act
    response = client.get("/goals?sort=id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"},
        {
            "id": 2,
            "title": "Work out"},
        {
            "id": 3,
            "title": "Call my parents often"},
    ]

pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal_filter_by_title(client, three_goals):
    # Act
    data = {'title': 'Work out'}
    response = client.get("/goals", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 2,
            "title": "Work out"}
    ]

pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found(client):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    #raise Exception("Complete test")
    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {"details": "Not found"}
    assert Goal.query.get(1) == None


pytest.mark.skip(reason="No way to test this feature yet")
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

pytest.mark.skip(reason="test to be completed by student")
def test_update_goal(client, one_goal):

    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Updated Goal Title"
        }
    }

pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_with_missing_title(client, one_goal):
    # Act
    response = client.put("/goals/1", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body["details"] == "Invalid data"

pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    #raise Exception("Complete test")
    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body["details"] == "Not found"
    assert Goal.query.get(1) == None


pytest.mark.skip(reason="No way to test this feature yet")
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

    # Check that the goal was deleted
    response_body = client.get("/goals/1")

    #raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found(client):
    #raise Exception("Complete test")

    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {"details": "Not found"}
    assert Goal.query.get(1) == None


pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
