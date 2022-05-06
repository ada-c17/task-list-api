from flask import Blueprint, jsonify, abort, make_response, request
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

def create_task_dictionary(chosen_task):
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
    return task_dict


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
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200

@tasks_bp.route("", methods = ["POST"])
def create_one_task():
    request_body = request.get_json()
    try:

        chosen_task = Task( title = request_body["title"],
                    description = request_body["description"]
                    )
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(chosen_task)
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 201

@tasks_bp.route("/<task_id>", methods = ["PUT"])
def add_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    request_body = request.get_json()
    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
    except KeyError:
        return {
            "msg": "title and description are required"
        }, 400
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{chosen_task.title}" successfully deleted'
    }, 200