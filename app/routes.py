from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", method=["POST"])
def create_task():
    request_body = request.get_json()

    if request_body["title"] and request_body["description"]:
        new_task = Task.create(request_body)
    else:
        abort(make_response({"message": f"Task data is not valid"}, 400))
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(f"New task {new_task.title} "\
        "successfully created"), 201)