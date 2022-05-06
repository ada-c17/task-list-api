from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_id(task_id):
    try:
        task_id =  int(task_id)
    except:
        return abort(make_response(jsonify({'message': f"Invalid task: {task_id}"}), 400))
    task = Task.query.get(task_id)

    if task is None:
        return abort(make_response(jsonify({'message': f"Could not find task with id {task_id}"}), 404))
    return task       

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    if 'title' not in request_body or 'description' not in request_body:
        return {
            "details": "Invalid data"
        }, 400

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
    }}, 201

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        task_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
    })
    return jsonify(task_response), 200

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    one_task = validate_id(task_id)
    response = {
            "id": one_task.task_id,
            "title": one_task.title,
            "description": one_task.description,
            "is_complete": False
        }
    return jsonify({"task": response}), 200

@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_one_task(task_id):
    one_task = validate_id(task_id)
    request_body = request.get_json()
    if 'title' not in request_body or 'description' not in request_body:
        return {
            "details": "Invalid data"
        }, 400

    one_task.title = request_body["title"]
    one_task.description = request_body["description"]

    db.session.commit()

    response = {
        "id": one_task.task_id,
        "title": one_task.title,
        "description": one_task.description,
        "is_complete": False
    }
    return jsonify({"task": response}), 200

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    one_task = validate_id(task_id)
    db.session.delete(one_task)
    db.session.commit()

    return {"details": f'Task {one_task.task_id} "{one_task.title}" successfully deleted'}, 200


