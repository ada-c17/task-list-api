from app import db
from app.models.task import Task
from .routes_helpers import validate_id, error_message
from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy import asc,desc
from datetime import date
import os
import requests

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

# Get all tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all() 

    tasks_response = [task.to_json() for task in tasks]

    return make_response(jsonify(tasks_response), 200)

# Get one task
@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_id("Task", id)
    response_body = {}
    response_body["task"] = task.to_json()
    
    return make_response(jsonify(response_body), 200)

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.create(request_body)
    except KeyError:
        message = "Invalid data"
        return error_message(message, 400)

    db.session.add(new_task)
    db.session.commit()

    response_body = {}
    response_body["task"] = new_task.to_json()

    return make_response(jsonify(response_body), 201)

# Update Task
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_id("Task", id)
    request_body = request.get_json()

    try:
        task.update(request_body)
    except KeyError:
        message = "Invalid data"
        return error_message(message, 400)

    db.session.commit()
    
    response_body = {}
    response_body["task"] = task.to_json()

    return make_response(jsonify(response_body), 200)

# PATCH REQUEST - MARK COMPLETE
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_id("Task", id)

    task.completed_at = date.today()

    db.session.commit()

    response_body = {}
    response_body["task"] = task.to_json()

    # endpoint for slack bot to post message
    SLACK_POST_PATH = "https://slack.com/api/chat.postMessage"

    # slack bot message
    slack_message = f"Someone just completed the task {task.title}"

    # headers
    headers = {"Authorization": os.environ.get("SLACK_BOT_KEY")}

    # query_params
    query_params = {
        "channel":"task-notifications",
        "text": slack_message}

    requests.post(SLACK_POST_PATH, params=query_params, headers=headers)

    return make_response(jsonify(response_body), 200)

# PATCH REQUEST - MARK INCOMPLETE
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_id("Task", id)

    task.completed_at = None

    db.session.commit()

    response_body = {}
    response_body["task"] = task.to_json()
    
    return make_response(jsonify(response_body), 200)

# DELETE
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_id("Task", id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({'details':f'Task {task.id} "{task.title}" successfully deleted'}), 200)