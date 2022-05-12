# def test_get_all_tasks_with_no_records(client):
#     # Act
#     response = client.get("/tasks")

#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body == []


# def test_get_all_tasks(client, three_tasks):
#     # Act
#     response = client.get("/tasks")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body == [
#         {
#             "id": 1,
#             "title": "Water the garden 🌷",
#             "description": "",
#             "is_complete": "false"
#         },
#         {
#             "id": 2,
#             "title": "Answer forgotten email 📧",
#             "description": "",
#             "is_complete": "false"
#         },
#         {
#             "id": 3,
#             "title": "Pay my outstanding tickets 😭",
#             "description": "",
#             "is_complete": "false"
#         }

#     ]


# def test_one_task(client, one_task):
#     # Act
#     response = client.get("/tasks/1")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body == {
#         "task": {
#             "id": 1,
#             "title": "Go on my daily walk 🏞",
#             "description":  "Notice something new every day",
#             "is_complete": False
#         }
#     }


# def test_get_one_task_with_no_records(client):
#     # Act
#     response = client.get("/tasks/1")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 404
#     assert response_body == {"message": "task 1 not found"}


# def test_create_one_planet(client):
#     # Act
#     response = client.post("/tasks", json={
#         "name": "Mars",
#         "description": "Is Bruno Mars counted as Mars?",
#         "color": "orange"
#     })
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 201
#     assert response_body == "Planet Mars successfully created"
