from app import db
from app.models.task import Task
from .task_helper_routes import make_task_safely, replace_task_safely, get_task_by_id
from .routes_helper import success_msg
from flask import Blueprint, jsonify, abort, make_response, request

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    new_task = make_task_safely(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    task_list = [task.to_dict() for task in tasks]

    return jsonify(task_list), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_task_by_id(task_id)
    
    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    request_body = request.get_json()

    task = get_task_by_id(task_id)
    replace_task_safely(task, request_body)

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_task_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return success_msg(f'Task {task.task_id} "{task.title}" successfully deleted', 200)
