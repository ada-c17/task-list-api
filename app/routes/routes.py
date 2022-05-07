from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from .helpers import validate_task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task.from_json(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_json()}), 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = [task.to_json() for task in tasks]
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return jsonify({'task':task.to_json()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.update_task(request_body)

    db.session.commit()

    return jsonify({'task':task.to_json()}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details":f'Task {task_id} "{task.title}" successfully deleted'} ), 200
        



