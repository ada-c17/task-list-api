from flask import Blueprint, jsonify
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", strict_slashes=False, methods =["GET"])
def get_tasks():
    tasks = Task.query.all()
    response = []
    for task in tasks:
        response.append({"id": task.task_id, 
                        "title": task.title, 
                        "description": task.description, 
                        "is_complete": bool(task.completed_at)})
    
    return jsonify(response), 200

