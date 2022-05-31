from typing import Literal
from flask import Blueprint, Response, jsonify, request
from app import db
from datetime import datetime
from app.models.task import Task
from app.commons import validate_and_get_by_id, get_filtered_and_sorted
from app.slack_interaction import notify

QueryParam = str  # for type annotations

###############
# Task routes #
###############

task_bp = Blueprint('tasks', __name__, url_prefix = '/tasks')

@task_bp.route('', methods = ['GET'])
def get_tasks() -> tuple[Response, Literal[200]]:
    '''Queries DB for Tasks and returns result as JSON data.'''

    if not request.args:
        return jsonify(Task.query.all()), 200
    return jsonify(get_filtered_and_sorted(Task, request.args)), 200

@task_bp.route('', methods = ['POST'])
def create_task() -> tuple[Response, Literal[201]]:
    '''Passes request JSON data to Task.create() and saves result to DB.
    
    Returns details of created Task instance as JSON data.
    '''

    new_task = Task.create(request.get_json())
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task}), 201

@task_bp.route('/<task_id>', methods = ['GET'])
def get_task_by_id(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Task and returns details as JSON data.'''

    return jsonify({'task': validate_and_get_by_id(Task, task_id)}), 200

@task_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Passes request JSON data to Task.update() and saves result to DB.
    
    Returns details of updated Task instance as JSON data.
    '''

    task = validate_and_get_by_id(Task, task_id)
    task.update(request.get_json())
    db.session.commit()

    return jsonify({'task': task}), 200

@task_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Task instance and deletes it if found.'''
    
    task = validate_and_get_by_id(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': (f'Task {task_id} "{task.title}" '
                                f'successfully deleted')}), 200

@task_bp.route('/<task_id>/mark_complete', methods = ['PATCH'])
def mark_task_complete(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Sets value of completed_at attribute on specified Task instance.
    
    Returns details of updated Task instance as JSON data.
    '''
    
    task = validate_and_get_by_id(Task, task_id) 
    task.completed_at = datetime.utcnow()
    db.session.commit()

    notify(task.title, 'mark_complete') # Slack notification
    return jsonify({'task': task}), 200

@task_bp.route('/<task_id>/mark_incomplete', methods = ['PATCH'])
def mark_task_incomplete(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Unsets value of completed_at attribute on specified Task instance.
    
    Returns details of updated Task instance as JSON data.
    '''

    task = validate_and_get_by_id(Task, task_id)    
    task.completed_at = None
    db.session.commit()

    notify(task.title, 'mark_incomplete') # Slack notification
    return jsonify({'task': task}), 200