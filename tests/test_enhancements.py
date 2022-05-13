import pytest

def test_invalid_sort_parameter_is_ignored(client, three_tasks):
    response = client.get('/tasks?sort=foo')
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            'id': 1,
            'title': "Water the garden 🌷",
            'description': "",
            'is_complete': False
        },
        {
            'id': 2,
            'title': "Answer forgotten email 📧",
            'description': "",
            'is_complete': False
        },
        {
            'id': 3,
            'title': "Pay my outstanding tickets 😭",
            'description': "",
            'is_complete': False
        }
    ]

def test_invalid_sort_still_allows_filtering(client, three_tasks, completed_task):
    response = client.get('/tasks?sort=foo&is_complete=True')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            'id': 4,
            'title': "Go on my daily walk 🏞",
            'description': "Notice something new every day",
            'is_complete': True
        }
    ]

def test_title_can_be_fuzzy_filtered(client, three_tasks):
    response = client.get('/tasks?title=Water')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            'id': 1,
            'title': "Water the garden 🌷",
            'description': "",
            'is_complete': False
        }
    ]

def test_description_can_be_fuzzy_filtered(client, three_tasks, completed_task):
    response = client.get('/tasks?description=new')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            'id': 4,
            'title': "Go on my daily walk 🏞",
            'description': "Notice something new every day",
            'is_complete': True
        }
    ]

def test_query_can_both_filter_and_sort(client, three_tasks, completed_task):
    response = client.get('/tasks?sort=asc&is_complete=False')
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            'id': 2,
            'title': "Answer forgotten email 📧",
            'description': "",
            'is_complete': False
        },
        {
            'id': 3,
            'title': "Pay my outstanding tickets 😭",
            'description': "",
            'is_complete': False
        },
        {
            'id': 1,
            'title': "Water the garden 🌷",
            'description': "",
            'is_complete': False
        }
    ]

def test_string_timestamp_can_be_converted(client, three_tasks):
    response = client.put('/tasks/2', json={
        'description': 'Inbox zero.',
        'completed_at': 'Monday, May 9, 2022'
        })
    response_body = response.get_json()

    assert response.status_code == 200
    assert 'task' in response_body
    assert response_body == {
        'task': {
            'id': 2,
            'title': "Answer forgotten email 📧",
            'description': "Inbox zero.",
            'is_complete':  True
        }
    }

def test_invalid_string_timestamp_returns_error(client, three_tasks):
    response = client.put('/tasks/2', json={
        'description': 'Inbox zero.',
        'completed_at': 'The other day'
        })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == ("Input value for attribute of task was invalid: "
                            "Value of completed_at must be str, datetime, or "
                            "None. If provided as a string, the timestamp "
                            "must be in a standard date and time format.")
