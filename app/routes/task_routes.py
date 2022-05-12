from flask import Blueprint, request, make_response, jsonify
import requests
from app.models.task import Task
from app import db
from datetime import datetime
import os
import requests
from app.routes.helper_routes import get_filtered_tasks, validate_datetime, validate_id, validate_request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = validate_request(request, "title", "description")
    new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=validate_datetime(request_body)
            )

    db.session.add(new_task)
    db.session.commit()
    return make_response({"task": new_task.to_dict()}, 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = get_filtered_tasks(request)
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

# GET /<task_id>
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_id(Task, task_id)
    return {"task": task.to_dict_with_goal_id()}

# PUT /<task_id>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)
    request_body = validate_request(request, "title", "description")
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return make_response(jsonify({"task": task.to_dict()}))

# DELETE /<task_id>
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})

# MARK COMPLETE
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.commit()

    channel_name = "task-notifications"
    headers = {"Authorization": os.environ.get("SLACK_AUTHORIZATION")}
    text = f"Someone just completed the task {task.title}"
    url = f"https://slack.com/api/chat.postMessage?channel={channel_name}&text={text}&pretty=1"
    requests.post(url, headers=headers)

    return make_response({"task": task.to_dict()})

# MARK INCOMPLETE
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return make_response({"task": task.to_dict()})