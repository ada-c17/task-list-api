from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from os import abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
    )

    db.session.add(new_task)
    db.session.commit()

    response = {"id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.is_complete}
    
    return jsonify({"task": response}), 201

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    task_response = []
    tasks = Task.query.all()
    for task in tasks:
        task_response.append({
            'title': task.task_id,
            'description': task.description,
            'completed_at': task.completed_at
        })
    return jsonify(task_response)