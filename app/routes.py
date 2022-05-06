from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route('', methods=["POST"])
def create_a_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], 
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()
    return {
        "task_id": new_task.task_id,
        "msg": f"Successfully created task with id {new_task.task_id}"
    }, 201
