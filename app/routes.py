import os

import requests
from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return jsonify(
            {
                "details": "Invalid data"
            }), 400
    else:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body.get("completed_at"))

    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete()
        }
    }
    return make_response(jsonify(response_body), 201)


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify({"details": "Invalid data"}, 400)))

    task = Task.query.get(task_id)
    if task:
        return task

    abort(make_response({"details": "Item not found"}, 404))


def update_completed_at(task, completed_at):

    task.completed_at = completed_at
    db.session.commit()
    return jsonify(
        {
            "task": to_dict(task)
        }
    ), 200


def to_dict(task):
    return {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete()
    }


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args
    if "sort" in params:
        if params["sort"] == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif params["sort"] == "desc":
            tasks = Task.query.order_by(Task.title.desc())

        # task_title = params["title"]
        # tasks = Task.query.filter_by(title = task_title)
    else:
        tasks = Task.query.all()

    response = []

    for task in tasks:
        response.append(to_dict(task))
    return jsonify(response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return jsonify({"task": to_dict(task)}), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")

    db.session.commit()

    return jsonify({"task": to_dict(task)}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify(
        {"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200


def send_notification(title):
    message = f'Someone just completed the task {title}'
    query = {"channel": "task-notifications", "text": f'"{message}"'}
    headers = {"Authorization": os.environ.get("SLACK_TOKEN")}
    requests.get(os.environ.get("SLACK_URL"), headers=headers, params=query)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_completed_at_attribute(task_id):
    task = validate_task(task_id)
    rs = update_completed_at(task, datetime.utcnow())
    send_notification(task.title)
    return rs


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_incompleted_tasks(task_id):
    task = validate_task(task_id)
    return update_completed_at(task, None)
