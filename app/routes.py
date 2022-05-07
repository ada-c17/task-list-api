from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app import db


bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=("POST",))
def create_task():
    request_body = request.get_json()
    
    new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": Task.to_dict(new_task)}, 201)


@bp.route("", methods=("GET",))
def read_tasks():
    """
    As a client, I want to be able to make a `GET` request to `/tasks` when there is at least one saved task and get this response:

    `200 OK`
    """
    tasks = Task.query.all()
    return jsonify([Task.to_dict(task) for task in tasks])