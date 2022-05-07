from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"Message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"Message":f"Task {task_id} not found"}, 404))

    return task

def make_task_dict(task):
    task_dict = {"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
    }}
    if task.completed_at:
        task_dict["task"]["is_complete"] = True
    else:
        task_dict["task"]["is_complete"] = False

    return task_dict

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    response_body = []

    for task in tasks: # make dict then append response_body list
        response = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
        }
        if task.completed_at:
            response["is_complete"] = True
        else:
            response["is_complete"] = False
        response_body.append(response)
        
    print(response_body)

    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    task_dict = make_task_dict(task)
    return jsonify(task_dict), 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"])
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    task_dict = make_task_dict(new_task)

    return jsonify(task_dict), 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    task_dict = make_task_dict(task)

    return jsonify(task_dict), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200



