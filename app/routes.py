from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
# from os import abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(
            {"message": f"Task {task_id} invalid.  Must be numerical"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)})
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_single_task(task_id):
    task = validate_task_id(task_id)
    return{"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)}}


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": bool(new_task.completed_at)}}), 201)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    found_task = validate_task_id(task_id)

    request_body = request.get_json()

    found_task.title = request_body["title"]
    found_task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task":
                                  {"id": found_task.task_id,
                                   "title": found_task.title,
                                   "description": found_task.description,
                                   "is_complete": bool(found_task.completed_at)}}), 200)
