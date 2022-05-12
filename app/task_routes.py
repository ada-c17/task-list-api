from app import db
from app.models.task import Task
from app.validate_helper import validate_element
from flask import Blueprint, request, make_response, jsonify
from datetime import datetime
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


#Get all tasks
@tasks_bp.route("", methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    
    return make_response(jsonify(tasks_response), 200)


#Get one task
@tasks_bp.route("<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = validate_element(task_id, "task")

    return jsonify({"task": task.to_json()}), 200


#POST one task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.create_task(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201


#UPDATE one task
@tasks_bp.route("<task_id>", methods=['PUT'])
def update_one_task(task_id):
    task = validate_element(task_id, "task")
    request_body = request.get_json()

    task.title = request_body['title']
    task.description = request_body['description']

    db.session.commit()
    
    return make_response(jsonify({"task" : task.to_json()}), 200)


#Delete one task
@tasks_bp.route('<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = validate_element(task_id, "task")

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200)


#Mark one task complete
@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    task = validate_element(task_id, "task")
    
    task.completed_at = datetime.now()
    db.session.commit()

    slack_api_url = "https://slack.com/api/chat.postMessage"
    params = {
        "channel" : "task-notifications",
        "text" : f"Someone just completed the task {task.title}"
    }
    headers = {
        "Authorization" : f"Bearer {os.environ.get('SLACK_API_HEADER')}"
    }
    requests.get(url=slack_api_url, params=params, headers=headers)
    
    return make_response(jsonify({"task" : task.to_json()}))



#Mark one task incomplete
@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = validate_element(task_id, "task")

    task.completed_at = None
    db.session.commit()

    return make_response(jsonify({"task" : task.to_json()}))



