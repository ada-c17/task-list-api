from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    comleted_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)