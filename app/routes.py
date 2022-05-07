import datetime
from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response, abort
from .helpers import validate_task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.create(request_body)
        db.session.add(new_task)
        db.session.commit()

    except KeyError:
        return abort(make_response(jsonify({"details": "Invalid data"}), 400))

    return make_response(jsonify(new_task.to_json()), 201)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    # tasks_response = [task.to_json() for task in tasks]
    tasks_response = []

    for task in tasks:
        complete = None
        if task.completed_at == None:
            complete = False
        else:
            complete = True
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": complete
        })

    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_task(task_id)
    return make_response(jsonify(task.to_json()), 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return make_response(jsonify(task.to_json()), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_update(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    if task.completed_at == None:
        task.completed_at = datetime.datetime.now()

    db.session.commit()
    return make_response(jsonify(task.to_json()), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_update(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    if task.completed_at != None:
        task.completed_at = None

    db.session.commit()
    return make_response(jsonify(task.to_json()), 200)
