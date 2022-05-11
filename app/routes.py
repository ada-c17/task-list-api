from flask import Blueprint, request, make_response, abort, jsonify
import requests
from sqlalchemy import asc
from app.models.task import Task
from app import db
from datetime import date
import os
import requests
import json

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# VALIDATE ID
def validate_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response(jsonify(f"Task {task_id} is invalid"), 400))
    task = Task.query.get(task_id)
    if not task:
        abort(make_response(jsonify(f"Task {task_id} not found"), 404))
    return task

# VALIDATE REQUEST
def validate_request(request):
    request_body = request.get_json()
    try:
        request_body["title"]
        request_body["description"]
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400)) 
    return request_body

# POST /tasks
@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = validate_request(request)
    try:
        completion_time = request_body["completed_at"]
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at = completion_time
        )
    except KeyError:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
        )
    db.session.add(new_task)
    db.session.commit()
    return make_response({"task": new_task.to_dict()}, 201)

# GET /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    # Pull query parameters from url
    title_param = request.args.get("title")
    description_param = request.args.get("description")
    is_complete_param = request.args.get("is_complete")
    sort_param = request.args.get("sort")
    # start the query
    tasks = Task.query
    # build up the search criteria based on params present
    if title_param:
        tasks = tasks.filter_by(title=title_param)
    if description_param:
        tasks = tasks.filter_by(description=description_param)
    if is_complete_param:
        tasks = tasks.filter_by(completed_at=is_complete_param)
    if sort_param == "asc":
        tasks = tasks.order_by(Task.title.asc())
    elif sort_param == "desc":
        tasks = tasks.order_by(Task.title.desc())
    # execute the search and return all records that meet the criteria built
    tasks = tasks.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

# GET /<task_id>
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_id(task_id)
    return {"task": task.to_dict()}

# PUT /<task_id>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(task_id)
    request_body = validate_request(request)
    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at = request_body["is_complete"]
    db.session.commit()
    return make_response(jsonify({"task": task.to_dict()}))

# DELETE /<task_id>
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})

# MARK COMPLETE
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_id(task_id)
    task.completed_at = date.today()
    db.session.commit()

    # Sends message to channel to congratulate on task completion
    channel_name = "task-notifications"
    headers = {"Authorization": os.environ.get("SLACK_AUTHORIZATION")}
    text = f"Someone just completed the task {task.title}"
    url = f"https://slack.com/api/chat.postMessage?channel={channel_name}&text={text}&pretty=1"
    response = requests.post(url, headers=headers)

    return make_response({"task": task.to_dict()})

# MARK INCOMPLETE
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_id(task_id)
    task.completed_at = None
    db.session.commit()
    return make_response({"task": task.to_dict()})