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