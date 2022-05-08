from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from .helpers import validate_task
from datetime import datetime, timezone

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
    sort_query = request.args.get("sort")

    if sort_query:
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title)
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())

    else:
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

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f"Task {task.task_id} \"{task.title}\""\
                        " successfully deleted"}), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)

    time = datetime.now(timezone.utc)

    task.completed_at = time

    db.session.commit()

    return jsonify({"task": task.to_json()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    if task.completed_at:
        task.completed_at = None

    db.session.commit()

    return jsonify({"task": task.to_json()}), 200
