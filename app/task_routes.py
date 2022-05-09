from app import db
from flask import Blueprint, jsonify, request, make_response
from app.models.task import Task
from .task_routes_helper import check_task_exists, try_to_make_task, post_task_to_slack
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

# Create a Task
@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = try_to_make_task(request_body)

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"task": new_task.to_json()}), 201

# Get Tasks
@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    sort_value = request.args.get("sort")

    if sort_value == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_value == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif not sort_value:
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

@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_task_complete(task_id):
    task = check_task_exists(task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()

    post_task_to_slack(task)

    return make_response(jsonify({"task": task.to_json()}), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_task_incomplete(task_id):
    task = check_task_exists(task_id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}), 200)

# Delete Task
@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = check_task_exists(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200