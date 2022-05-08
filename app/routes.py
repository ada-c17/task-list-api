from app import db
from flask import Blueprint, jsonify, request, make_response
from app.models.task import Task
from .routes_helper import check_task_exists

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

# Create a Task
@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.make_task(request_body)

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"task": new_task.to_json()}), 201

# Get Tasks
@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = [task.to_json() for task in tasks]

    return jsonify(tasks_response), 200

# Get a single Task
@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = check_task_exists(task_id)

    return make_response(jsonify({"task": task.to_json()}), 200)

# Update Task
@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = check_task_exists(task_id)
    request_body = request.get_json()

    task.update_task(request_body)

    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}), 200)

# Delete Task
@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = check_task_exists(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200