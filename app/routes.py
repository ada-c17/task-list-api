from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from .models.task import Task
from datetime import datetime
import requests, os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
#check task is found
    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))
    else:
        return task

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    
    sort_param = request.args.get("sort")

    if sort_param:
        if sort_param == "asc":
            tasks = Task.query.order_by(Task.title).all()
        elif sort_param == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_task(task_id)

    response_body = {"task": task.to_dict()}

    return make_response(jsonify(response_body), 200)


@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body.get("completed_at")
            )
    except: 
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}

    return make_response(jsonify(response_body), 201)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except KeyError as err:
        return make_response(f"Key error {err}", 400)
    
    db.session.commit()

    response_body = {"task": task.to_dict()}

    return make_response(jsonify(response_body), 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.utcnow()
    
    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"

    SLACK_API_KEY = os.environ.get("SLACK_API_TOKEN")

    response_body = {"task": task.to_dict()}
    headers = {"Authorization": f"Bearer {SLACK_API_KEY}",
    "Content-Type": "application/json"}
    json_body = {"channel": "task-notifications",
    "text": f"Someone just completed the task {task.title}"}

    requests.post(path, headers=headers, json=json_body)

    return make_response(jsonify(response_body), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    
    db.session.commit()

    response_body = {"task": task.to_dict()}

    return make_response(jsonify(response_body), 200)