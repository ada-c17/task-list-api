from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from datetime import datetime
import os
import requests

# Slackbot API functionality data, SLACK_BOT_TOKEN in .env
SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    task = Task(
        title = request_body["title"],
        description = request_body["description"],
    )
    
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]

    db.session.add(task)
    db.session.commit()

    response = task.task_response()

    return make_response(jsonify({"task": response}), 201)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    response = []

    # Order by sorted if "sort" in argument
    sort_by = request.args.get('sort')
    if sort_by == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_by == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    for task in tasks:
        response.append(task.task_response())

    return make_response(jsonify(response), 200)


# Helper function to validate task id is integer and exists
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message":f"Task id '{task_id}' is invalid"}
        abort(make_response(jsonify(response), 400))

    task = Task.query.get(task_id)

    if not task:
        response = {"message":f"Task id '{task_id}' not found"}
        abort(make_response(jsonify(response), 404))

    return task


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    response = task.task_response()

    return make_response(jsonify({"task": response}), 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = task.task_response()

    return make_response(jsonify({"task": response}), 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.utcnow()

    db.session.add(task)
    db.session.commit()

    # Define arguments to integrate Slackbot API chat.postMessage method
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    data = {
        "channel":  "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    
    # Slackbot "Grace's Slackbot" calls to SLACK_API_URL and posts message
    requests.post(SLACK_API_URL, headers=headers, data=data)

    response = task.task_response()
    return make_response(jsonify({"task": response}))


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    
    db.session.add(task)
    db.session.commit()

    response = task.task_response()

    return make_response(jsonify({"task": response}))


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {
    "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
    }

    return make_response(jsonify(response), 200)