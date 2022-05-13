import os
import requests
from app import db
from distutils.log import error
from datetime import datetime
from app.models.task import Task
from app.routes_helper import validate_task, error_message
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def make_task(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError as err:
        return error_message("Invalid data", 400)

# POST /tasks
@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    
    new_task = make_task(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return{"task":new_task.to_dict()}, 201

# GET /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    sort_param = request.args.get("sort")

    if sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    else:
        tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            }
        )

    return jsonify(tasks_response)

# GET /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(Task, task_id)

    return{"task":task.to_dict()}, 200

# PUT /tasks/<task_id> 
@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_task_by_id(task_id):
    task = validate_task(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return{"task":task.to_dict()}, 200

# PATCH /tasks/<task_id>/mark_complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_with_id(task_id):
    task = validate_task(Task, task_id)
    task.completed_at = datetime.utcnow()

    db.session.commit() 
    print(post_slack_message(task.title))

    return{"task":task.to_dict()}, 200

# PATCH /tasks/<task_id>/mark_incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_incomplete_task(task_id):
    task = validate_task(Task, task_id)

    task.completed_at = None

    db.session.commit()
    return{"task":task.to_dict()}, 200

# DELETE /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = validate_task(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

def post_slack_message(text):
    channel = "task-notifications"
    return requests.post('https://slack.com/api/chat.postMessage',
    headers={"Authorization": os.environ.get("SLACK_BOT_TOKEN")},
    json={
        'channel': channel,
        'text': text
    }).json()
