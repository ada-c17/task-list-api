from wsgiref import headers
from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.models.task import Task
from app import db
from datetime import datetime
import os

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({'details': 'Invalid data'}, 400))
    
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({'details': f'No task with id {task_id}'}, 404))

    return task


def check_for_params():
    params = request.args
    if 'sort' in params:
        if params['sort'] == 'desc':
            tasks = Task.query.order_by(Task.title.desc()).all()
        elif params['sort'] == 'asc':
            tasks = Task.query.order_by(Task.title.asc()).all()
        else:
            tasks = Task.query.all()
    elif 'title' in params:
        tasks = Task.query.filter_by(title=params['title'])
    else:
        tasks = Task.query.all()
    return tasks


@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    new_task = Task.from_json(request_body)

    db.session.add(new_task)
    db.session.commit()

    rsp = {'task': new_task.to_json()}
    return jsonify(rsp), 201


@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = check_for_params()

    tasks_response = [task.to_json() for task in tasks]

    return jsonify(tasks_response), 200


@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = validate_task_id(task_id)
    rsp = {'task': task.to_json()}

    return jsonify(rsp), 200


@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': f'Task {task.id} \"{task.title}\" successfully deleted'}), 200


@tasks_bp.route('/<task_id>', methods=['PUT', 'PATCH'])
def update_one_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()
    task = task.from_json_to_update(request_body)

    db.session.commit()

    rsp = {'task': task.to_json()}
    return jsonify(rsp), 200


@tasks_bp.route('<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    daytime_completed = datetime.now()
    task = validate_task_id(task_id)
    task.completed_at = daytime_completed

    db.session.commit()

    rsp = {'task': task.to_json()}

    token_key = os.environ.get("SLACK_BOT_TOKEN")
    slack_url = "https://slack.com/api/chat.postMessage"
    body = {
            "text": f"Someone just completed the task {task.title}",
            "channel": "task-notifications"}

    auth_header = {"Authorization": token_key}

    requests.post(slack_url, params=body, headers=auth_header)

    return jsonify(rsp), 200


@tasks_bp.route('<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = validate_task_id(task_id)
    task.completed_at = None

    db.session.commit()

    rsp = {'task': task.to_json()}
    return jsonify(rsp), 200
