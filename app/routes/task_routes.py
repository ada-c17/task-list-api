from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db
from .routes_helper import get_record_by_id, make_task_safely, replace_task_safely
import os
import requests
from dotenv import load_dotenv

load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def post_completed_task_to_slack(task):
    API_KEY = os.environ.get('SLACKBOT_API_KEY')
    url = "https://slack.com/api/chat.postMessage"
    data = {"channel": "task-notifications", "text": f"Someone just completed the task {task.title}"}
    headers = {'Authorization' : f"Bearer {API_KEY}" }
    
    requests.post(url, data=data, headers=headers)

# POST /tasks
@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = make_task_safely(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

# GET /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_param = request.args.get("sort")

    if sort_param == 'asc':
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_param == 'desc':
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    result_list = [task.to_dict() for task in tasks]

    return jsonify(result_list)

# GET /tasks/<id>
@tasks_bp.route("/<id>", methods=["Get"])
def read_task_by_id(id):
    task = get_record_by_id(Task, id)
    return jsonify({"task":task.to_dict()})

# PUT /tasks/<id>
@tasks_bp.route("/<id>", methods=["PUT"])
def replace_task_by_id(id):
    request_body = request.get_json()
    task = get_record_by_id(Task, id)

    replace_task_safely(task, request_body)

    db.session.add(task)
    db.session.commit()

    return jsonify({"task":task.to_dict()})

# DELETE /tasks/<id>
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task_by_id(id):
    task = get_record_by_id(Task, id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'})

# PATCH /tasks/<id>/mark_complete
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def update_task_to_complete(id):
    task = get_record_by_id(Task, id)

    task.completed_at = datetime.now()

    db.session.commit()

    post_completed_task_to_slack(task)

    return jsonify({"task":task.to_dict()})

# PATCH /tasks/<id>/mark_incomplete
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def update_task_to_incomplete(id):
    task = get_record_by_id(Task, id)
    task.completed_at = None

    db.session.commit()

    return jsonify({"task":task.to_dict()})


