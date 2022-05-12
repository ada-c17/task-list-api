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
def test_get_goal_not_found(client):
    pass
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'details': 'No goal with id 1'}


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
    # Act
    response = client.put("/goals/1", json={
        'title': 'Updated goal to go outside daily'
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        'goal': {
            'id': 1,
            'title': 'Updated goal to go outside daily'
        }
    }

    goal = Goal.query.get(1)
    assert goal.title == 'Updated goal to go outside daily'


# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    response = client.put("/goals/1", json={
        'title': 'Updated goal to go outside daily'
    })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {'details': 'No goal with id 1'}


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

    # Check that the goal was deleted
    response = client.get("/goals/1")
    response_body = response.get_json()
    assert response.status_code == 404
    assert response_body == {'details': 'No goal with id 1'}


# @pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found(client):
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'details': 'No goal with id 1'}


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


def test_validate_goal_id(client):
    # Act
    response = client.get("/goals/one")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'details': 'Invalid data'}


def test_update_goal_missing_title(client, one_goal):
    # Act
    response = client.put("/goals/1", json={})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {'details': "Invalid data"}

    goal = Goal.query.get(1)
    assert goal.title == 'Build a habit of going outside daily'


def test_get_goals_sorted_asc(client, three_goals):
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
            "title": "Code everyday for at least 3 hours"},
        {
            "id": 2,
            "title": "Read one book in a month"}
        ]


def test_get_goals_sorted_desc(client, three_goals):
    # Act
    response = client.get("/goals?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Read one book in a month"},
        {
            "id": 3,
            "title": "Code everyday for at least 3 hours"},
        {
            "id": 1,
            "title": "Build a habit of going outside daily"}
        ]

def test_get_goals_sorted_invalid_params(client, three_goals):
    # Act
    response = client.get("/goals?sort=descc")
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
            "title": "Read one book in a month"},
        {
            "id": 3,
            "title": "Code everyday for at least 3 hours"}
        ]
