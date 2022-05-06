from app import db
from flask import Blueprint, jsonify, request, make_response
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

# Create a Task
@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"], 
                    description = request_body["description"])

    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify({"task": new_task.to_json()}), 201)

# Get Tasks
@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    pass

# Get a single Task
@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    pass

# Update Task
@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    pass

# Delete Task
@tasks_bp.rotue("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    pass