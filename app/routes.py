from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

# Create a new task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    task = Task(
        title = request_body["title"],
        description = request_body["description"]
    )

    db.session.add(task)
    db.session.commit()

    is_complete = True if task.completed_at else False

    response = {"id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete}
    
    return jsonify({"task": response}), 201

# Get all tasks
@tasks_bp.route("", methods=["GET"])
def get_tasks():
    task_response = []
    tasks = Task.query.all()

    for task in tasks:
        is_complete = True if task.completed_at else False
        task_response.append({
            'id': task.task_id,
            'title': task.title,
            'description': task.description,
            'is_complete': is_complete
        })
    return jsonify(task_response)

# Validate task id helper function
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task id '{task_id}' is invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task id '{task_id}' not found"}, 404))

    return task

# Get one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    is_complete = False

    is_complete = True if task.completed_at else False

    response = {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete
        }

    return jsonify({"task": response}), 200


# Update task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    is_complete = True if task.completed_at else False

    response = {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete
        }

    return make_response({"task": response})