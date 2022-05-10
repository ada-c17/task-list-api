from flask import Blueprint, request, make_response, abort, jsonify
from app import db
from app.models.task import Task
from sqlalchemy import desc, asc
from datetime import datetime
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Wave 1
# get all task list
@tasks_bp.route("", methods=["GET"])
def read_all_tast():

    # sort all tasts by title
    params = request.args
    if "sort" in params:
        if params["sort"].lower() == "desc" or params["sort"].lower() == "descending":
            chosen_task = Task.query.order_by( desc(Task.title) ).all()
        else:
            chosen_task = Task.query.order_by( asc(Task.title) ).all()
    else:     
        chosen_task = Task.query.all()
    # return empty list when no task in database
    if len(chosen_task) == 0:
        return jsonify([]), 200

    # return all tasts
    response_body = []
    for task in chosen_task:
        response_body.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })

    return jsonify(response_body), 200

# helper function to check task id
def validate_task_id(task_id):
    """
    Checking the id task from input:
        - return object task if id is integer
        - raise exception if id is not integer then return status code 400,
        but if the id not exist then return status code 404

    """
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"The task id {task_id} is invalid. The id must be integer."}, 400))
    
    tasks = Task.query.all()
    for task in tasks:
        if task.id == task_id:
            return task
    abort(make_response({"message": f"The task id {task_id} is not found"}, 404))

# get one task by id
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_task_by_id(task_id):
    chosen_task = validate_task_id(task_id)
    response_body = {
        "task": {
            "id": chosen_task.id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": bool(chosen_task.completed_at)
        }
    }
    return jsonify(response_body), 200

# helper function to check key dictionary exist or not
def validate_data_key_for_post_or_update():
    """Checking missing data key when post or update
        - raise exception if the key doesn't exist
        - return request object if the key exist
    """
    request_task = request.get_json()
    if "title" not in request_task or "description" not in request_task:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_task


# create one task
@tasks_bp.route("", methods=["POST"])
def creat_task():
    request_task = validate_data_key_for_post_or_update()
    new_task = Task(
        title = request_task["title"],
        description = request_task["description"]
    )
    if "completed_at" in request_task:
        new_task.completed_at = request_task["completed_at"]
    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }
    }
    return jsonify(response_body), 201


# update a task
@tasks_bp.route("<task_id>", methods=["PUT"])
def update_task(task_id):
    chosen_task = validate_task_id(task_id)
    request_task = validate_data_key_for_post_or_update()
    chosen_task.title = request_task["title"]
    chosen_task.description = request_task["description"]
    
    if "completed_at" in request_task:
        chosen_task.completed_at = request_task["completed_at"]

    db.session.commit()

    response_body = {
        "task": {
            "id": chosen_task.id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": bool(chosen_task.completed_at)
        }
    }

    return jsonify(response_body), 200

# delete task by id
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task_by_id(task_id):
    chosen_task = validate_task_id(task_id)
    db.session.delete(chosen_task)
    db.session.commit()
    response_body = {"details": f'Task {task_id} "{chosen_task.title}" successfully deleted'}
    return jsonify(response_body), 200

