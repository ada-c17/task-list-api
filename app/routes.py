from flask import Blueprint, jsonify
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_books():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        is_complete = True
        if task.competed_at is None:
            is_complete = False
        tasks_response.append({"id": task.id, "title": task.title, "description": task.description, "is_complete": is_complete})
    return jsonify(tasks_response)

