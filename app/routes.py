import json
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

from app.routes_helper import validate_task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"])
    except KeyError:
        abort(make_response(jsonify(dict(details="Invalid data")), 400))
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(dict(task=new_task.to_dict())), 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_param = request.args.get("sort")

    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    
    tasks_response = [task.to_dict() for task in tasks]

    return make_response(jsonify(tasks_response))

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task_data = validate_task(task_id)

    return make_response(jsonify(dict(task=task_data.to_dict())))

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_data = validate_task(task_id)
    request_body = request.get_json()

    task_data.title = request_body["title"]
    task_data.description = request_body["description"]

    db.session.commit()
    updated_task_data = Task.query.get(task_id)
    return make_response(jsonify(dict(task=updated_task_data.to_dict())))

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_data = validate_task(task_id)

    db.session.delete(task_data)
    db.session.commit()
    return make_response(jsonify(dict(details=f'Task {task_data.task_id} "{task_data.title}" successfully deleted'))) 