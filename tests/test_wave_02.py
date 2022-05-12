import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_asc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False},
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False}
    ]


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"},
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
    ]


def test_get_multiple_tasks_no_sorting_sorts_by_id(client, three_tasks):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"}
    ]


def test_get_tasks_invalid_sort_returns_error(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=blah")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid sort parameter 'blah'. Sort parameter may only be 'asc' or 'desc'."
    }


def test_get_tasks_filter_by_description(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?description=food")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "Give cats wet and dry food",
            "id": 2,
            "is_complete": False,
            "title": "Feed cats AM"},
        {
            "description": "Give cats wet food and pills",
            "id": 3,
            "is_complete": False,
            "title": "Feed cats PM"},
        {
            "description": "Make sure to eat food!",
            "id": 5,
            "is_complete": False,
            "title": "Make dinner"}
    ]

def test_get_tasks_filter_by_description_param_not_found_returns_message(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?description=chocolate")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {
        "details": "Search parameter 'chocolate' not found in any tasks."
    }


def test_get_tasks_filter_by_title(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=cats")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "description": "Give cats wet and dry food",
            "id": 2,
            "is_complete": False,
            "title": "Feed cats AM"},
        {
            "description": "Give cats wet food and pills",
            "id": 3,
            "is_complete": False,
            "title": "Feed cats PM"}
    ]

def test_get_tasks_filter_by_title_param_not_found_returns_message(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=chocolate")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {
        "details": "Search parameter 'chocolate' not found in any tasks."
    }


def test_get_tasks_filter_by_title_and_description(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=cats&description=give")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "description": "Give cats wet and dry food",
            "id": 2,
            "is_complete": False,
            "title": "Feed cats AM"},
        {
            "description": "Give cats wet food and pills",
            "id": 3,
            "is_complete": False,
            "title": "Feed cats PM"}
    ]

def test_get_tasks_filter_by_title_and_description_not_found_returns_message(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=chocolate&description=honey")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "details" in response_body
    assert response_body == {
        "details": "Search parameter 'chocolate' not found in any tasks."
    }



def test_get_tasks_filter_by_description_and_sort_ascending(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?description=make&sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "description": "Make sure to eat food!",
            "id": 5,
            "is_complete": False,
            "title": "Make dinner"},
        {
            "description": "Make sure the flowers grow!",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"}
    ]

def test_get_tasks_filter_by_description_and_sort_descending(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?description=make&sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "description": "Make sure the flowers grow!",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
        {
            "description": "Make sure to eat food!",
            "id": 5,
            "is_complete": False,
            "title": "Make dinner"}
    ]

def test_get_tasks_filter_by_description_and_sort_fail_returns_error(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?description=make&sort=blah")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid sort parameter 'blah'. Sort parameter may only be 'asc' or 'desc'."
    }


def test_get_tasks_filter_by_title_and_sort_ascending(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=cats&sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "description": "Give cats wet and dry food",
            "id": 2,
            "is_complete": False,
            "title": "Feed cats AM"},
        {
            "description": "Give cats wet food and pills",
            "id": 3,
            "is_complete": False,
            "title": "Feed cats PM"}
    ]

def test_get_tasks_filter_by_title_and_sort_descending(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=cats&sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "description": "Give cats wet food and pills",
            "id": 3,
            "is_complete": False,
            "title": "Feed cats PM"},
        {
            "description": "Give cats wet and dry food",
            "id": 2,
            "is_complete": False,
            "title": "Feed cats AM"}
    ]

def test_get_tasks_filter_by_title_and_sort_fail_returns_error(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=cats&sort=blah")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid sort parameter 'blah'. Sort parameter may only be 'asc' or 'desc'."
    }

def test_get_tasks_filter_by_title_and_description_sort_ascending(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=cats&description=give&sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "description": "Give cats wet and dry food",
            "id": 2,
            "is_complete": False,
            "title": "Feed cats AM"},
        {
            "description": "Give cats wet food and pills",
            "id": 3,
            "is_complete": False,
            "title": "Feed cats PM"}
    ]


def test_get_tasks_filter_by_title_and_description_sort_descending(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=cats&description=give&sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "description": "Give cats wet food and pills",
            "id": 3,
            "is_complete": False,
            "title": "Feed cats PM"},
        {
            "description": "Give cats wet and dry food",
            "id": 2,
            "is_complete": False,
            "title": "Feed cats AM"}
    ]

def test_get_tasks_filter_by_title_and_description_sort_fail_returns_error(client, five_tasks_with_description):
    # Act
    response = client.get("/tasks?title=cats&description=give&sort=blah")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid sort parameter 'blah'. Sort parameter may only be 'asc' or 'desc'."
    }