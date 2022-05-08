from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from .helpers import validate_task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if request_body.get("title") and request_body.get("description"):
        new_task = Task.create(request_body)
    else:
        abort(make_response({"details": "Invalid data"}, 400))
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_json()}), 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    task_response_body = []
    for task in tasks:
        task_response_body.append(task.to_json())

    return jsonify(task_response_body), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return jsonify({"task": task.to_json()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    if request_body.get("title") and request_body.get("description"):
        task.update(request_body)
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.commit()
    
    return jsonify({"task": task.to_json()}), 200