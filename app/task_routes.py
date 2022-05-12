


import os, requests
from datetime import datetime
from requests import request
from sqlalchemy import desc
from app import db
from app.models.task import Task
from app.helper import validate_task, validate_req_body_tasks
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

# POST
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not validate_req_body_tasks(request_body, "title", "description"):
        return {"details": "Invalid data"}, 400
    new_task = Task.create(request_body)
    db.session.add(new_task)
    db.session.commit()
    return { "task": new_task.to_json()}, 201

# GET all
@tasks_bp.route("", methods=["GET"])
def read_task():
    sort_query = request.args.get("sort")
    if sort_query == 'asc':
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query == 'desc':
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200

# GET one Task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)

    return { "task": task.to_json()}, 200

# UPDATE one Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.update(request_body)
    db.session.commit()
    return { "task": task.to_json()}, 200

# DELETE one Task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200

# PATCH 
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def patch_complete_task(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    token = os.environ.get("SLACK_API_KEY")
    header = {'Authorization': f'Bearer {token}'}
    params = {
        "channel": "C03F50XDCDA",
        "text": f"Someone just completed the task {task.title}"
    }
    slack_response = requests.post(url, params=params, headers=header)

    return {"task": task.to_json()}


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def patch_incomplete_task(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()
    return { "task": task.to_json()}, 200

        
    
