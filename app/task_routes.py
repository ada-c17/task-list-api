from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from .routes_helper import validate_task_id, create_message
from app import db
from datetime import datetime
import requests, os


bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=("POST",))
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        create_message("Invalid data", 400)
    task = Task.from_dict(request_body)
    db.session.add(task)
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 201)


@bp.route("/<task_id>", methods=("GET",))
def read_one_task(task_id):
    task = validate_task_id(task_id)
    return make_response(jsonify({"task": task.to_dict()}))


@bp.route("", methods=("GET",))
def read_all_tasks():
    title_query = request.args.get("sort")

    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    tasks_response = [task.to_dict() for task in tasks]

    return make_response(jsonify(tasks_response))


@bp.route("/<task_id>", methods=("PUT",))
def replace_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()
    task.override_task(request_body)
    db.session.commit()

    return jsonify({"task": task.to_dict()})


@bp.route("/<task_id>", methods=("DELETE",))
def delete_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()

    create_message(f'Task {task_id} "{task.title}" successfully deleted')


@bp.route("/<task_id>/mark_complete", methods=("PATCH",))
def mark_task_complete(task_id):
    task = validate_task_id(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()

    requests.post(
        url="https://slack.com/api/chat.postMessage", 
        data={
            "channel": "task-notifications", 
            "text": f"Someone just completed the task {task.title}"
        }, 
        headers={"Authorization": os.environ.get("token")}, 
    )

    return jsonify({"task": task.to_dict()})


@bp.route("/<task_id>/mark_incomplete", methods=("PATCH",))
def mark_task_incomplete(task_id):
    task = validate_task_id(task_id)
    task.completed_at = None
    db.session.commit()
    return jsonify({"task": task.to_dict()})