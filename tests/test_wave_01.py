from app.models.task import Task
import pytest
from datetime import datetime, date


#pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_no_saved_tasks(client):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


#pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_one_saved_tasks(client, one_task):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    ]


#pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task(client, one_task):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }


#pytest.mark.skip(reason="No way to test this feature yet")
def test_get_task_not_found(client):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    #raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************
    assert response_body == {"message": "The task id 1 is not found"}

#pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": False
        }
    }
    new_task = Task.query.get(1)
    assert new_task
    assert new_task.title == "A Brand New Task"
    assert new_task.description == "Test Description"
    assert new_task.completed_at == None


#pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": False
        }
    }
    task = Task.query.get(1)
    assert task.title == "Updated Task Title"
    assert task.description == "Updated Test Description"
    assert task.completed_at == None


#pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task_not_found(client):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    #raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************
    assert response_body == {"message": "The task id 1 is not found"}

#pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_task(client, one_task):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    }
    assert Task.query.get(1) == None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_task_not_found(client):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    #raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************

    assert response_body == {"message": "The task id 1 is not found"}
    assert Task.query.all() == []


#pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_must_contain_title(client):
    # Act
    response = client.post("/tasks", json={
        "description": "Test Description"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Task.query.all() == []


#pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_must_contain_description(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Task.query.all() == []

# test code coverage
def test_read_task_is_not_integer_id(client):
    # Act
    response = client.get("tasks/one")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": f"The task id one is invalid. The id must be integer."}


# Optional Enhancement Testing
def test_get_tasks_filter_by_title(client, three_tasks):
    # Act
    data= {"title": "Water the garden 🌷"}
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 200
    assert response_body == [{
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False
    }]


def test_get_tasks_sort_by_title_desc(client, three_tasks):
    # Act
    data= {"sort": "desc"}
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False 
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False 
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False 
        },
    ]


def test_get_tasks_sort_by_title_sensitive_case_descending(client, three_tasks):
    # Act
    data= {"sort": "Descending"}
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False 
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False 
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False 
        },
    ]


def test_get_tasks_sort_by_title_asc(client, three_tasks):
    # Act
    data= {"sort": "asc"}
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False 
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False 
        },
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False 
        }
    ]


def test_get_tasks_sort_by_title_no_sort_type(client, three_tasks):
    # Act
    data= {"sort": ""}
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False 
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False 
        },
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False 
        }
    ]


def test_get_tasks_by_id_for_a_goal_sort_asc(client, three_tasks_belong_to_one_goal):
    # Act
    data= {
        "sort": "asc",
        "goal_id": 1
    }
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        }
    ]

def test_get_tasks_by_id_for_a_goal_sort_desc(client, three_tasks_belong_to_one_goal):
    # Act
    data= {
        "sort": "desc",
        "goal_id": 1
    }
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        }
    ]


def test_get_tasks_by_id_for_a_goal_sort_sensitive_case_asc(client, three_tasks_belong_to_one_goal):
    # Act
    data= {
        "sort": "Ascending",
        "goal_id": 1
    }
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        }
    ]
    

def test_get_tasks_by_id_for_a_goal_sort_sensitive_case_desc(client, three_tasks_belong_to_one_goal):
    # Act
    data= {
        "sort": "DESCENDING",
        "goal_id": 1
    }
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        }
    ]


def test_get_tasks_by_id_for_invalid_goal_sort_desc(client, three_tasks_belong_to_one_goal):
    # Act
    data= {
        "sort": "desc",
        "goal_id": "one"
    }
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "The goal id one is invalid. The id must be integer."}


def test_get_tasks_by_id_for_none_exist_goal_sort_asc(client, three_tasks_belong_to_one_goal):
    # Act
    data= {
        "sort": "asc",
        "goal_id": 2
    }
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "The goal id 2 is not found"}


def test_get_tasks_by_id_for_a_goal_sort_with_empty(client, three_tasks_belong_to_one_goal):
    # Act
    data= {
        "sort": "",
        "goal_id": 1
    }
    response = client.get("/tasks", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "goal_id": 1,
            "description": "",
            "is_complete": False 
        }
    ]



def test_create_task_with_completed_at(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": "Fri, 13 May 2022 00:00:00 GMT"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": True
        }
    }
    new_task = Task.query.get(1)
    assert new_task
    assert new_task.title == "A Brand New Task"
    assert new_task.description == "Test Description"
    assert new_task.completed_at.strftime("%m/%d/%Y") == "05/13/2022"



def test_update_task_with_completed_at(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
        "completed_at": "Fri, 13 May 2022 00:00:00 GMT"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": True
        }
    }
    task = Task.query.get(1)
    assert task.title == "Updated Task Title"
    assert task.description == "Updated Test Description"
    assert task.completed_at.strftime("%m/%d/%Y") == "05/13/2022"