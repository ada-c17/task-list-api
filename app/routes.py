from flask import Blueprint, jsonify
from app.models.task import Task
from app import db
from app.helper import validate_task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", strict_slashes=False, methods =["GET"])
def get_tasks():
    tasks = Task.query.all()
    response = []
    for task in tasks:
        response.append({"id": task.id, 
                        "title": task.title, 
                        "description": task.description, 
                        "is_complete": bool(task.completed_at)})
    
    return jsonify(response), 200

@task_bp.route("/<task_id>", strict_slashes=False, methods =["GET"])
def get_task(task_id):
    tasks = Task.query.all()
    response = {}
    task = validate_task(task_id)
    
    response["task"] = {"id": task.id, 
                        "title": task.title, 
                        "description": task.description, 
                        "is_complete": bool(task.completed_at)}

    return jsonify(response), 200