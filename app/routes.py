from flask import Blueprint,jsonify
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        if task.completed_at is None:
            task_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            })
        else: 
            task_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": True
            })
    return jsonify(task_response)