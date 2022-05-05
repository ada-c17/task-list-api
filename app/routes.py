from sys import prefix
from flask import Blueprint, request, jsonify, make_response
from .models.task import Task


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    
    response_body = []
    for task in tasks:
        response_body.append(id=task.id, title=task.title, description=task.description)
    
    return jsonify(response_body), 200

