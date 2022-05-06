from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

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
    db.session.add(new_task)
    db.session.commit()
    
    response = {
        "task" : 
            {
                "is_complete" : False,
                "description" : new_task.description,
                "title" : new_task.title,
                "id" : new_task.task_id
            }
        }

    return response, 201

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append(
            {
                "is_complete" : False,
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
        return {
        "task" : 
            {
                "is_complete" : False,
                "description" : task.description,
                "title" : task.title,
                "id" : task.task_id
            }
        }, 200

    return task

@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    if isinstance(task, Task):
        task.title = request_body["title"]
        task.description = request_body["description"]
        db.session.commit()

        return {
        "task" : 
            {
                "is_complete" : False,
                "description" : task.description,
                "title" : task.title,
                "id" : task.task_id
            }
        }, 200

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
