from app import db
from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], 
                    description=request_body["description"], completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return {"task": {"id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": False}}, 201
