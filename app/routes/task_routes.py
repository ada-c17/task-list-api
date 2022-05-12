from psycopg2 import DataError
from app import db
from app.models.task import Task
from .routes_helpers import validate_id, error_message, send_msg_to_channel, sort_records
from flask import Blueprint, request, make_response, jsonify
from datetime import date
import time

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

# Get all tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    if request.args.get("sort"):
        sort_query = request.args.get("sort")
        tasks = sort_records(Task, sort_query)
    else:
        tasks = Task.query.all() 

    tasks_response = [task.to_json() for task in tasks]

    return make_response(jsonify(tasks_response), 200)

# Get One Task - already dry
@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_id("Task", id)
    response_body = {}
    response_body["task"] = task.to_json()
    
    return make_response(jsonify(response_body), 200)

# Create Task - already dry
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.create(request_body)
    except KeyError:
        message = "Invalid data"
        return error_message(message, 400)
    except DataError:
        message = "Invalid data"
        return error_message(message, 400)

    db.session.add(new_task)
    db.session.commit()

    response_body = {}
    response_body["task"] = new_task.to_json()

    return make_response(jsonify(response_body), 201)

# Update Task - already dry
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_id("Task", id)
    request_body = request.get_json()

    try:
        task.update(request_body)
    except KeyError:
        message = "Invalid data"
        return error_message(message, 400)

    db.session.commit()
    
    response_body = {}
    response_body["task"] = task.to_json()

    return make_response(jsonify(response_body), 200)

# Mark Task Complete - this be dry
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task = validate_id("Task", id)
    task.completed_at = time.strftime("%Y-%m-%d")

    db.session.commit()

    response_body = {}
    response_body["task"] = task.to_json()

    send_msg_to_channel(task)

    return make_response(jsonify(response_body), 200)

# PATCH REQUEST - MARK INCOMPLETE
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task = validate_id("Task", id)

    task.completed_at = None

    db.session.commit()

    response_body = {}
    response_body["task"] = task.to_json()
    
    return make_response(jsonify(response_body), 200)

# DELETE
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_id("Task", id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({'details':f'Task {task.id} "{task.title}" successfully deleted'}), 200)