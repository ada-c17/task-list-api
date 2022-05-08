from flask import Blueprint, jsonify, request
from sqlalchemy import true
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    task_list = []

    for task in tasks:
        task_list.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })
    
    return jsonify(task_list)