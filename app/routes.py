from asyncio import tasks
import imp
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    try:
        request_body = request.get_json()
        new_task = Task(title=request_body['title'], description=request_body['description'])
    except KeyError:
        return jsonify({'details': 'Invalid data'}), 400

    db.session.add(new_task)
    db.session.commit()

    rsp = {'task': {
            'id': new_task.task_id,
            'title': new_task.title,
            'description': new_task.description,
            'is_complete': False
        }}

    return jsonify(rsp), 201

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append({
                'id': task.task_id,
                'title': task.title,
                'description': task.description,
                'is_complete': False
            })
    
    return jsonify(tasks_response), 200

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = Task.query.get(task_id)
    rsp = {"task": {
        'id': task.task_id,
        'title': task.title,
        'description': task.description,
        'is_complete': False
    }}
    return jsonify(rsp), 200

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': f'Task {task.task_id} \"{task.title}\" successfully deleted'}), 200

@tasks_bp.route('/<task_id>', methods=['PUT', 'PATCH'])
def update_one_task(task_id):
    task = Task.query.get(task_id)
    request_body = request.get_json()

    try:
        task.title = request_body['title']
        task.description = request_body['description']
    except KeyError:
        return jsonify({'details': 'Invalid data'}), 400
    
    db.session.commit()

    rsp = {"task": {
        'id': task.task_id,
        'title': task.title,
        'description': task.description,
        'is_complete': False
    }}

    return jsonify(rsp), 200