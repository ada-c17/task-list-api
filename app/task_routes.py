
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from .helper import validate_task, get_sorted_obj, call_slack
from datetime import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Create a task
@task_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    if not request_body.get("title") or not request_body.get("description"):
        return {"details": "Invalid data"}, 400
    new_task = Task.create(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_json()}, 201

# Get all tasks, sort by task name
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks=get_sorted_obj()
    tasks_response = []
    tasks_response=[task.to_json() for task in tasks]

    return jsonify(tasks_response), 200


# get_one_task
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return {"task": task.to_json()}, 200

# UPDATE task
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return {"task": task.to_json()}, 200

# Update: Mark Incomplete on a Completed Task


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)
    if task.completed_at:
        task.completed_at = None
        db.session.commit()

    return read_one_task(task_id)

# Update: Mark Complete on an Incompleted Task
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)
    if not task.completed_at:

        call_slack(task.title)
        task.completed_at = datetime.utcnow()
        db.session.commit()
    return read_one_task(task_id)


# DELETE Task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% goals start here
