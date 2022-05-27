from flask import Blueprint, jsonify, make_response, request
from .models.task import Task
from .routes_helper_functions import *
from app import db
from datetime import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=("POST",))
def post_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"])
    except KeyError:
        error_message(f"Invalid data", 400)

    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.one_task_to_dict()), 201

@task_bp.route("", methods=("GET",))
def get_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    result_list = [task.to_dict() for task in tasks]

    return jsonify(result_list), 200

@task_bp.route("/<task_id>", methods=("GET",))
def get_one_task(task_id):
    task = validate_task(task_id)

    return jsonify(task.one_task_to_dict()), 200

@task_bp.route("/<task_id>", methods=("PUT",))
def put_one_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.replace_details(request_body)

    db.session.commit()

    return jsonify(task.one_task_to_dict()), 200

@task_bp.route("/<task_id>", methods=("DELETE",))
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify(dict(details=f'Task {task.task_id} "{task.title}" successfully deleted'))), 200

@task_bp.route("/<task_id>/mark_complete", methods=("PATCH",))
def patch_one_task_as_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.utcnow()

    db.session.commit()

    return jsonify(task.one_task_to_dict()), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=("PATCH",))
def patch_one_task_as_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None

    db.session.commit()

    return jsonify(task.one_task_to_dict()), 200
