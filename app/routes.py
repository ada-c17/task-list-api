from flask import Blueprint, jsonify
from app.models.task import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('', methods=['GET'])
def handle_tasks():
    tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append({
            'title': task.title,
            'description': task.description
        })
    return jsonify(tasks_response)