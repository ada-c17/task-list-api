from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route('', methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], 
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()
    return {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
    }, 201

@task_bp.route('', methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
        })
    return jsonify(tasks_response)

@task_bp.route('', methods=["GET"])
def get_one_task():
    pass

@task_bp.route('', methods=["PUT"])
def update_task():
    pass

@task_bp.route('', methods=["DELETE"])
def delete_task():
    pass
