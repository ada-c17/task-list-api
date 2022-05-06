from asyncio import tasks
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from .helpers import validate
from datetime import date


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# POST ROUTES


@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_task = Task.create(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_json()}, 201)

# GET ROUTES


@ tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_order = request.args.get("sort")

    if sort_order == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_order == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = [task.to_json() for task in tasks]

    return jsonify(response), 200


@ tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate(task_id)
    return make_response({"task": task.to_json()}, 200)

# PUT ROUTES


@ tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate(task_id)
    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return make_response({"task": task.to_json()}, 200)

# DELETE ROUTES


@ tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_planet(task_id):
    task = validate(task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)

# PATCH ROUTES


@ tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate(task_id)
    task.completed_at = date.today()

    db.session.commit()
    return make_response({"task": task.to_json()}, 200)


@ tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate(task_id)
    task.completed_at = None

    db.session.commit()
    return make_response({"task": task.to_json()}, 200)
