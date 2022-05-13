from unittest.mock import patch
from flask import Blueprint, jsonify, request, make_response, abort
from pytest import param
from app.models.task import Task
from app import db
from datetime import datetime
import os
import requests


tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')


@tasks_bp.route('', methods=['POST'])
def create_a_task():
    request_body = request.get_json()

    if 'completed_at' in request_body:
        completed_at = request_body['completed_at']
    else:
        completed_at = None

    try:
        task = Task(title=request_body['title'],
                        description=request_body['description'],
                        completed_at=completed_at)
    except:
        return {'details': 'Invalid data'}, 400
    
    db.session.add(task)
    db.session.commit()
    
    return {'task': task.to_dict()}, 201


@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    task_list = []
    for task in tasks:
        task_list.append(task.to_dict())

    return jsonify(task_list), 200


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({'details': f'Invalid task id: {task_id}. Task id must be an integer'}), 400

    task = Task.query.get(task_id)

    if task is None:
        task_not_found = {'details': f'Could not find task id {task_id}'}
        abort(make_response(jsonify(task_not_found), 404))
        
    return task
    

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)
    
    return {'task': task.to_dict()}, 200
        

@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = validate_task(task_id)
    
    request_body = request.get_json()
    try:
        task.title = request_body['title']
        task.description = request_body['description']
    
    except KeyError:
        return jsonify({'details': 'Request must include both title and description'}), 400
    
    db.session.commit()

    return {'task': task.to_dict()}, 200


@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    task = validate_task(task_id)
    
    task.completed_at = datetime.now()
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    message = f'Someone just completed the task {task.title}'
    params = {'channel': 'task-notifications', 'text': message}
    headers = {'Authorization': f'Bearer {os.environ.get("SLACK_API_KEY")}'}

    requests.post(url, params=params, headers=headers)

    return {'task': task.to_dict()}, 200


@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    return {'task': task.to_dict()}, 200


@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': f'Task {task.task_id} \"{task.title}\" successfully deleted'}), 200

