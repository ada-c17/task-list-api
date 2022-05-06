from crypt import methods
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

# routes
@tasks_bp.route("", methods=['POST'])
def create_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"])
    except KeyError:
        return {"details" : "Invalid data"}, 400

    db.session.add(new_task)
    db.session.commit()
    return {
        "task":
        {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
            }
    }, 201


@tasks_bp.route("", methods=['GET'])
def get_all_task():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    return jsonify(tasks_response), 200

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = get_task_or_abort(task_id)
    return {
        "task":
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
            }
    }, 200

@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = get_task_or_abort(task_id)
    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.is_complete = False
    
    except KeyError:
        return {
            "msg" : "title and description are required" 
        }, 400
    
    db.session.commit()
    # check valid input after commits
    task = get_task_or_abort(task_id)
    return {
        "task":
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
            }
    }, 200

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task = get_task_or_abort(task_id)
    db.session.delete(task)
    db.session.commit()

    return {
        "details" : f'Task {task.id} "{task.title}" successfully deleted'
    }, 200