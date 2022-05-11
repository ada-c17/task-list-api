from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app import db
import datetime


bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=("POST",))
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        create_message("Invalid data", 400)
    # could change the above to a try and except
    task = Task.from_dict(request_body)

    db.session.add(task)
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 201)


@bp.route("/<task_id>", methods=("GET",))
def read_one_task(task_id):
    task = validate_task_id(task_id)
    return make_response(jsonify({"task": task.to_dict()}), 200)


@bp.route("", methods=("GET",))
def read_all_tasks():
    title_query = request.args.get("sort")

    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    tasks_response = [task.to_dict() for task in tasks]

    return make_response(jsonify(tasks_response), 200)


@bp.route("/<task_id>", methods=("PUT",))
def replace_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()
    # might want to put this into a try and except
    task.override_task(request_body)
    
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


@bp.route("/<task_id>", methods=("DELETE",))
def delete_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()
    create_message(f"Task {task_id} \"{task.title}\" successfully deleted", 200)


@bp.route("/<task_id>/mark_complete", methods=("PATCH",))
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()
    task_keys = request_body.keys()

    if "name" in task_keys:
        task.name = request_body["name"]

    if "description" in task_keys:
        task.description = request_body["description"]

    task.completed_at = datetime.datetime.now()

    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        create_message("Invalid data", 400)

    task = Task.query.get(task_id)

    if not task:
        create_message("Task 1 not found", 404)
    return task


def create_message(details_info, status_code):
    abort(make_response({"details": details_info}, status_code))