from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({"msg" : f"'{task_id}' is invalid"}), 400
    
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"message" : f"Could not find '{task_id}'"}), 404
    return task