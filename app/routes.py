from flask import Blueprint, jsonify, abort, make_response
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"msg": f"Invalid id: {task_id}"}
        abort(make_response(jsonify(response), 400))

    chosen_task = Task.query.get(task_id)    

    if chosen_task is None:
        response = {"msg": f"Could not find task with id {task_id}"}
        abort(make_response(jsonify(response), 404))
    return chosen_task


@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        if task.completed_at is None:
            task_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            })
        else: 
            task_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": True
            })
    return jsonify(task_response), 200

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    task_dict= {}
    if chosen_task.completed_at is None:
        task_dict["task"] = {
            "id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": False
        }
    else: 
        task_dict["task"] = {
            "id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": True
        }
    return jsonify(task_dict), 200
