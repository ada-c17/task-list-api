from app import db
from app.models.task import Task
from .routes_helpers import validate_id, send_msg_to_channel, sort_records, validate_data
from flask import Blueprint, request, jsonify
import time

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    if request.args.get("sort"):
        sort_query = request.args.get("sort")
        tasks = sort_records(Task, sort_query)
    else:
        tasks = Task.query.all() 

    tasks_response = [task.to_json() for task in tasks]

    return jsonify(tasks_response), 200

@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_id(Task, id)
    response_body = {}
    response_body["task"] = task.to_json()
    
    return jsonify(response_body), 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = validate_data(Task.create, request_body)

    db.session.add(new_task)
    db.session.commit()

    response_body = {}
    response_body["task"] = new_task.to_json()

    return jsonify(response_body), 201

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_id(Task, id)
    request_body = request.get_json()

    validate_data(task.update, request_body)

    db.session.commit()
    
    response_body = {}
    response_body["task"] = task.to_json()

    return jsonify(response_body), 200

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task = validate_id(Task, id)
    task.completed_at = time.strftime("%Y-%m-%d")

    db.session.commit()

    response_body = {}
    response_body["task"] = task.to_json()

    send_msg_to_channel(task)

    return jsonify(response_body), 200

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task = validate_id(Task, id)

    task.completed_at = None

    db.session.commit()

    response_body = {}
    response_body["task"] = task.to_json()
    
    return jsonify(response_body), 200

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_id(Task, id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({'details':f'Task {task.id} "{task.title}" successfully deleted'}), 200