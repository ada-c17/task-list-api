from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from datetime import datetime
import sys
import os
import requests
from dotenv import load_dotenv
load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(
            {"message": f"Task {task_id} invalid.  Must be numerical"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort")
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)})
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_single_task(task_id):
    task = validate_task_id(task_id)
    task_reply = {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)}}
    if task.goal_id:
        task_reply["task"]["goal_id"] = task.goal_id
    return task_reply


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"])
    except KeyError:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": bool(new_task.completed_at)}}, 201


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    found_task = validate_task_id(task_id)

    request_body = request.get_json()

    found_task.title = request_body["title"]
    found_task.description = request_body["description"]
    if "completed_at" in request_body:
        found_task.completed_at = request_body["completed_at"]
    db.session.commit()

    return {"task":
            {"id": found_task.task_id,
             "title": found_task.title,
             "description": found_task.description,
             "is_complete": bool(found_task.completed_at)}}, 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_status(task_id):
    found_task = validate_task_id(task_id)

    found_task.completed_at = datetime.now()

    db.session.commit()

    message = f"Someone just completed task {found_task.title}"

    headers = {"Authorization": "Bearer " + SLACK_TOKEN}
    params = {"channel": "task-notifications", "text": message}

    requests.post('https://slack.com/api/chat.postMessage',
                  data=params, headers=headers)

    return {"task":
            {"id": found_task.task_id,
             "title": found_task.title,
             "description": found_task.description,
             "is_complete": bool(found_task.completed_at)}}, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task_status(task_id):
    found_task = validate_task_id(task_id)

    found_task.completed_at = None

    db.session.commit()

    return {"task":
            {"id": found_task.task_id,
             "title": found_task.title,
             "description": found_task.description,
             "is_complete": bool(found_task.completed_at)}}, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    found_task = validate_task_id(task_id)

    db.session.delete(found_task)
    db.session.commit()

    return jsonify({"details": f'Task {found_task.task_id} "{found_task.title}" successfully deleted'})
