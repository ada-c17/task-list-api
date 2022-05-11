from crypt import methods
from datetime import datetime
from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# helper functions
def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg":f"Invalid id {task_id}"}
        abort(make_response(jsonify(rsp), 400))

    task = Task.query.get(task_id)
    if task is None:
        rsp = {"msg":f"Could not find task with id {task_id}"}
        abort(make_response(jsonify(rsp), 404))
    return task

def mark_completed_at(task_id, completed_at):
    task = get_task_or_abort(task_id)
    task.completed_at = completed_at
    db.session.commit()
    return jsonify(
        {
            "task": to_dict(task)
        }
    ), 200

def to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete()
    }

# routes
@tasks_bp.route("", methods=['POST'])
def create_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body.get("completed_at"))
    except KeyError:
        return {"details" : "Invalid data"}, 400

    db.session.add(new_task)
    db.session.commit()
    return jsonify(
        {
            "task": to_dict(new_task)
        }
    ), 201


@tasks_bp.route("", methods=['GET'])
def get_all_task():
    params = request.args
    if "sort" in params and "asc" == params["sort"]:
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif "sort" in params and "desc" == params["sort"]:
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(to_dict(task))

    return jsonify(tasks_response), 200


@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = get_task_or_abort(task_id)
    return jsonify(
        {
            "task": to_dict(task)
        }
    ), 200


@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = get_task_or_abort(task_id)
    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body.get("completed_at")
    
    except KeyError:
        return {
            "msg" : "title and description are required" 
        }, 400
    
    db.session.commit()
    # check valid input after commits
    task = get_task_or_abort(task_id)

    return jsonify(
        {
            "task": to_dict(task)
        }
    ), 200


@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task = get_task_or_abort(task_id)
    db.session.delete(task)
    db.session.commit()

    return {
        "details" : f'Task {task.id} "{task.title}" successfully deleted'
    }, 200


@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_as_complete_one_task(task_id):
    return mark_completed_at(task_id, datetime.utcnow())


@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_as_incomplete_one_task(task_id):
    return mark_completed_at(task_id, None)
    