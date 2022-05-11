from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import asc
from app.models.task import Task
from app import db


bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=("POST",))
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    # task = Task(title=request_body["title"], description=request_body["description"])
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
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


@bp.route("/<task_id>", methods=("DELETE",))
def delete_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()
    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"details": "Task 1 not found"}, 404))
    return task