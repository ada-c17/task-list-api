import requests
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from .helper import validate_task
from sqlalchemy import asc, desc
from datetime import datetime
from dotenv import load_dotenv
import os

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
load_dotenv()

# CREATE task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        if 'completed_at' in request_body:
            new_task = Task.create_complete(request_body)
        else:
            new_task = Task.create_incomplete(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.add(new_task)
    db.session.commit()

    response_body = {}
    response_body['task'] = new_task.to_json()

    return make_response(jsonify(response_body), 201)


# GET ALL tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == 'asc':
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == 'desc':
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200

# GET one task
@tasks_bp.route("/<task_id>", methods=["GET"])  
def read_one_task(task_id):
    task = validate_task(task_id)
    return make_response({"task": task.to_json()}, 200)

# UPDATE one task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    try:
        task.update(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.commit()

    response_body = {}
    response_body['task'] = task.to_json()

    return make_response(jsonify(response_body), 200)
    

# DELETE one task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details":f'Task {task.task_id} "{task.title}" successfully deleted'})), 200
    

# Mark task as complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)

    path = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("SLACK_API")
    head = {"Authorization":API_KEY}

    query_params = {
        "channel": "task-notifications",
        "text": "Someone just completed the task My Beautiful Task"
    }

    task.completed_at = datetime.today()
    req = requests.post(path, headers=head,params=query_params)

    db.session.commit()

    response_body = {}
    response_body['task'] = task.to_json()

    return make_response(jsonify(response_body), 200)

# Mark task as incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None

    db.session.commit()

    response_body = {}
    response_body['task'] = task.to_json()

    return make_response(jsonify(response_body), 200)

    



    
