from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db
from app.helper import validate_id, error_message, post_to_slack
import datetime


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", strict_slashes=False, methods=["GET"])
def get_tasks():
    sort_order = request.args.get("sort")
    if sort_order == 'asc':
        #sort ascending
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_order == 'desc':
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = [task.to_json() for task in tasks]
    return jsonify(response), 200


@task_bp.route("", strict_slashes=False, methods=["POST"])
def create_task():
    request_body = request.get_json()

    try: 
        new_task = Task.from_json(request_body)
    except KeyError:
        error_message("Invalid data", 400)

    db.session.add(new_task)
    db.session.commit()

    response = {"task": new_task.to_json()}
    return jsonify(response), 201


@task_bp.route("/<task_id>", strict_slashes=False, methods=["GET"])
def get_task(task_id):
    task = validate_id(Task, task_id)
    response = {"task": task.to_json()}
    return jsonify(response), 200


@task_bp.route("/<task_id>", strict_slashes=False, methods=["PUT"])
def update_task(task_id):
    request_body = request.get_json()
    task = validate_id(Task, task_id)
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")

    db.session.commit()

    response = response = {"task": task.to_json()}
    return jsonify(response), 200


@task_bp.route("/<task_id>", strict_slashes=False, methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task, task_id)
    response = {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}
    db.session.delete(task)
    db.session.commit()
    return jsonify(response), 200


@task_bp.route("/<task_id>/mark_complete", strict_slashes=False, methods=["PATCH"])
def mark_complete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = datetime.datetime.now()
    db.session.commit()

    post_to_slack(task)
    response = {"task": task.to_json()}
    return jsonify(response), 200


@task_bp.route("/<task_id>/mark_incomplete", strict_slashes=False, methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = None
    db.session.commit()

    response = {"task": task.to_json()}
    return jsonify(response), 200
