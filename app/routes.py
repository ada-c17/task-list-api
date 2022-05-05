from flask import Blueprint, jsonify, request, abort, make_response
from .models.task import Task
from app import db

task_bp = Blueprint("task_bp",__name__, url_prefix="/tasks" )
# Create: POST 
def create_task():
    pass 
    # request body: {"title": "A Brand New Task", "description": "Test Description"}
    # task Must contain title and description, else return: 
    # {"details": "Invalid data"}, 400
    # successful response body: {
#         "task": {
#             "id": 1,
#             "title": "A Brand New Task",
#             "description": "Test Description",
#             "is_complete": False
#         } }, 201

# Read: GET
def get_all_tasks():
    pass
def get_one_task(): # need this?
    pass

# example response body, status:
#            { "id": 1,
#             "title": "Go on my daily walk 🏞",
#             "description": "Notice something new every day",
#             "is_complete": False }, 200
# 

# Update: PUT
def update_task():
    pass
# request body:
#        { "title": "Updated Task Title",
#         "description": "Updated Test Description"}

#response_body == {"task": {
#             "id": 1,
#             "title": "Updated Task Title",
#             "description": "Updated Test Description",
#             "is_complete": False
#         } }, 200


# Delete: DELETE
def delete_task():
    pass
# response body: {"details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'}
# 404 if not found
