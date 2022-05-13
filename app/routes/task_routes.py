from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from app import db
from datetime import datetime
from app.routes.helper_routes import get_filtered_tasks, validate_id, validate_request


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = validate_request(request, "title", "description")
    new_task = Task.create(request_body)
    db.session.add(new_task)
    db.session.commit()
    return make_response({"task": new_task.to_dict()}, 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = get_filtered_tasks(request)
    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_id(Task, task_id)
    return {"task": task.to_dict_with_goal_id()}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)
    request_body = validate_request(request, "title", "description")
    task.update(request_body)
    db.session.commit()
    return make_response(jsonify({"task": task.to_dict()}))

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.commit()
    task.congrats_post()
    return make_response({"task": task.to_dict()})

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return make_response({"task": task.to_dict()})