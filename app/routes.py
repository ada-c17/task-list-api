from flask import Blueprint, jsonify, request, make_response
from app.models.task import Task
from app import db
from app.helper import validate_task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", strict_slashes=False, methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    response = []
    for task in tasks:
        response.append({"id": task.id, 
                        "title": task.title, 
                        "description": task.description, 
                        "is_complete": bool(task.completed_at)})
    
    return jsonify(response), 200


@task_bp.route("/<task_id>", strict_slashes=False, methods=["GET"])
def get_task(task_id):
    tasks = Task.query.all()
    response = {}
    task = validate_task(task_id)
    
    response["task"] = {"id": task.id, 
                        "title": task.title, 
                        "description": task.description, 
                        "is_complete": bool(task.completed_at)}

    return jsonify(response), 200


@task_bp.route("", strict_slashes=False, methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body.get("title"),
                    description = request_body.get("description"),
                    completed_at = request_body.get("completed_at"))

    db.session.add(new_task)
    db.session.commit()

    response = {}
    response["task"] = {"id": new_task.id,
                        "title": new_task.title,
                        "description": new_task.description,
                        "is_complete": bool(new_task.completed_at)}
    return jsonify(response), 201


@task_bp.route("/<task_id>", strict_slashes=False, methods=["PUT"])
def update_task(task_id):
    request_body = request.get_json()
    task = validate_task(task_id)
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")

    db.session.commit()

    response = {}
    response["task"] = {"id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": bool(task.completed_at)}

    return jsonify(response), 200