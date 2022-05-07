from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from sqlalchemy import desc

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def make_task_safely(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError as err:
        error_message(f"Invalid data", 400)

def update_task_safely(task, data_dict):
    try:
        return task.replace_details(data_dict)
    except KeyError as err:
        error_message(f"Invalid data", 400)

def validate_task_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)
    task = Task.query.get(id)
    if task:
        return task
    error_message(f"No task with ID {id}. SORRY.", 404)

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task=make_task_safely(request_body)

    db.session.add(new_task)
    db.session.commit()

    task_response = {"task":new_task.to_dict()}

    return jsonify(task_response), 201

@task_bp.route("", methods=["GET"])
def get_tasks():
    sort_param = request.args.get("sort")
    if sort_param == "asc":
        tasks = Task.query.order_by("title")
    elif sort_param == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    result_list = [task.to_dict() for task in tasks]
    return jsonify(result_list)

@task_bp.route("/<id>", methods=["GET"])
def get_task_by_id(id):
    task = validate_task_id(id)
    result = {"task": task.to_dict()}
    return jsonify(result)

@task_bp.route("<id>", methods=["PUT"])
def update_task(id):
    task = validate_task_id(id)
    request_body = request.get_json()
    updated_task = update_task_safely(task, request_body)

    db.session.commit()

    return jsonify({"task":updated_task})

@task_bp.route("<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task_id(id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details":f'Task {id} "{task.title}" successfully deleted'})