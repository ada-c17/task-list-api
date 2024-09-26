import pytest

def test_incorrect_args_for_task_sort_query(client):
    # Act
    response = client.get("/tasks?sort=nope")
    response_body = response.get_json()
    # Assert
    assert response_body == {
        "details":"Our sort selection is limited to: asc and desc"
        }

def test_incorrect_args_for_goal_sort_query(client):
    # Act
    response = client.get("/tasks?sort=nope")
    response_body = response.get_json()
    # Assert
    assert response_body == {
        "details":"Our sort selection is limited to: asc and desc"
        }

def test_get_goals_sorted_asc(client, three_goals):
    # Act
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "title": "Bake a birthday cake"},
        {
            "id": 1,
            "title": "Build a habit of going outside daily"},
        {
            "id": 2,
            "title": "Run at a marathon"}
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
            "title": "Run at a marathon"},
        {
            "id": 1,
            "title": "Build a habit of going outside daily"},
        {
            "id": 3,
            "title": "Bake a birthday cake"}
    ]

def test_get_task_invalid_input(client):
    # Act
    response = client.get("/tasks/hello_books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details":"Task is invalid"}

def test_get_goal_invalid_input(client):
    # Act
    response = client.get("/goals/hello_books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details":"Goal is invalid"}