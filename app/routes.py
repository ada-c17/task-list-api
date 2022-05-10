from flask import Blueprint, jsonify, request 
from app import db
from app.models.task import Task
from sqlalchemy import desc, asc
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({"msg" : f"'{task_id}' is invalid"}), 400
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message" : f"Could not find '{task_id}'"}), 404
    return task

def format_response(task):
    response = {
    "task" : 
        {
            "is_complete" : bool(task.completed_at),
            "description" : task.description,
            "title" : task.title,
            "id" : task.task_id
        }
    }
    return response

@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        return {
            "details" : "Invalid data"
        }, 400

    new_task = Task (
        description = request_body['description'],
        title = request_body['title']
    )

    if "completed_at" in request_body:
        new_task.completed_at = request_body['completed_at']

    db.session.add(new_task)
    db.session.commit()
    
    return format_response(new_task), 201


@tasks_bp.route('', methods=['GET'])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.order_by(asc(Task.title)).all()

    tasks_response = []

    for task in tasks:
        tasks_response.append(
            {
                "is_complete" : bool(task.completed_at),
                "description" : task.description,
                "title" : task.title,
                "id" : task.task_id
            }
        )

    return jsonify(tasks_response), 200


@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)

    if isinstance(task, Task):
        return format_response(task), 200
    return task


@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    if isinstance(task, Task):
        task.title = request_body["title"]
        task.description = request_body["description"]
        db.session.commit()

        if "completed_at" in request_body:
            task.completed_at = request_body['completed_at']

        return format_response(task), 200
    return task

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = validate_task(task_id)
    if isinstance(task, Task):
        db.session.delete(task)
        db.session.commit()
        return {
            "details" : f'Task {task_id} "{task.title}" successfully deleted'
        }
    return task

@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete(task_id):
    task = validate_task(task_id)

    if isinstance(task, Task):
        task.completed_at = datetime.utcnow()
        db.session.commit()
        return format_response(task), 200
    return task

@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    if isinstance(task, Task):
        task.completed_at = None
        db.session.commit()
        return format_response(task), 200
    return task

