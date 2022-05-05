from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# POST ROUTES


@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid Request", 400)
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(new_task.to_json()), 201)
