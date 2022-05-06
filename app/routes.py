from os import abort
from flask import Blueprint, jsonify, request, make_response, abort
from sqlalchemy import desc, asc
from app import db
from datetime import datetime
from app.models.task import Task

task_bp = Blueprint('tasks', __name__, url_prefix = '/tasks')

@task_bp.route('', methods = ['GET'])
def get_all_tasks():
    if not request.args:
        all_tasks = [task.to_json() for task in Task.query.all()]
    else:
        params = dict(request.args)
        sort_style = params.pop('sort', None)
        if sort_style and len(params) > 0:
            all_tasks = [task.to_json() for task in Task.query.filter_by(**params).order_by(getattr(Task.title,sort_style)())]
        elif sort_style:
            all_tasks = [task.to_json() for task in Task.query.order_by(getattr(Task.title,sort_style)())]
        else:
            all_tasks = [task.to_json() for task in Task.query.filter_by(**params)]

    return jsonify(all_tasks), 200

@task_bp.route('', methods = ['POST'])
def create_task():
    task_details = request.get_json()
    # Validate and clean input
    if 'title' not in task_details or 'description' not in task_details:
        abort(make_response(jsonify({"details": "Invalid data"}),400))
    if 'completed_at' not in task_details:
        task_details['completed_at'] = None
    
    new_task = Task(
        title = task_details['title'],
        description = task_details['description'],
        completed_at = task_details['completed_at']
        )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task.to_json()}), 201

@task_bp.route('/<task_id>', methods = ['GET'])
def get_task_by_id(task_id):
    task = Task.validate_id(task_id)

    return jsonify({'task': task.to_json()}), 200

@task_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id):
    task = Task.validate_id(task_id)
    updated_details = request.get_json()
    
    for k,v in updated_details.items():
        setattr(task, k, v)
    
    db.session.commit()

    return jsonify({'task': task.to_json()}), 200

@task_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = Task.validate_id(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': f'Task {task_id} "{task.title}" successfully deleted'}), 200

@task_bp.route('/<task_id>/mark_complete', methods = ['PATCH'])
def mark_task_complete(task_id):
    task = Task.validate_id(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()

    return jsonify({'task': task.to_json()}), 200

@task_bp.route('/<task_id>/mark_incomplete', methods = ['PATCH'])
def mark_task_incomplete(task_id):
    task = Task.validate_id(task_id)
    task.completed_at = None
    db.session.commit()

    return jsonify({'task': task.to_json()}), 200