from flask import Blueprint, jsonify, request, abort, make_response
from .models.task import Task
from app import db

task_bp = Blueprint("task_bp",__name__, url_prefix="/tasks" )

# Helper Functions
def complete_or_not(task):
    if task.completed_at is not None:
        return True
    else:
        return False

# completed_at = db.Column(db.DateTime, default=None)

# def validate_task(title):
#     try:
#         type(title) is str
#     except:
#         abort(make_response({"details": "Invalid data"}, 400))
#     task = Task.query.get(task_id)
    


# Create: POST 
@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(title=request_body['title'], description=request_body['description'])
    is_complete = complete_or_not(new_task) # use helper function to obain T/F
    db.session.add(new_task)
    db.session.commit()

    response =  {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
        } 
        }
    return jsonify(response), 201

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
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    pass

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    pass

# example response body, status:
#            { "id": 1,
#             "title": "Go on my daily walk 🏞",
#             "description": "Notice something new every day",
#             "is_complete": False }, 200
# 

# Update: PUT
@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
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
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    pass
# response body: {"details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'}
# 404 if not found
