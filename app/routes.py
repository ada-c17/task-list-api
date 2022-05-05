from os import abort
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task

task_bp = Blueprint('tasks', __name__, url_prefix = '/tasks')

@task_bp.route('', methods = ['GET'])
def get_all_tasks():
    if not request.args:
        all_tasks = [task.to_json() for task in Task.query.all()]
    else:
        all_tasks = [task.to_json() for task in Task.query.filter_by(**request.args)]

    return jsonify(all_tasks), 200

@task_bp.route('', methods = ['POST'])
def create_task():
    task_details = request.get_json()
    # Validate and clean input
    if 'title' not in task_details or 'description' not in task_details:
        abort(make_response(jsonify({"details": "Invalid data"}),400))

    new_task = Task(
        title = task_details['title'],
        description = task_details['description'],
        completed_at = None
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