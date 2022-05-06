from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
# from .helpers import validate_planet

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.create_task(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_json()}), 201


