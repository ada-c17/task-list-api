from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from .route_helpers import fetch_task
from sqlalchemy import asc, desc


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task(title = request_body["title"], description = request_body["description"])
        db.session.add(new_task)
        db.session.commit()
    except:
        abort(make_response(jsonify({"details":f"Invalid data"}), 400))
    return make_response(jsonify({"task": new_task.to_json()}), 201)

@task_bp.route("", methods=["GET"])
def fetch_all_tasks():

    sort = request.args.get("sort")
    if sort == "asc":
        tasks = Task.query.filter_by().order_by(Task.title.asc())
    elif sort == "desc":
        tasks = Task.query.filter_by().order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(task.to_json())
    return make_response(jsonify(task_response),200)

@task_bp.route("/<task_id>", methods=["GET"])
def fetch_a_task(task_id):
    task = fetch_task(task_id)
    return make_response(jsonify({"task": task.to_json()}), 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_a_task(task_id):
    
    task = fetch_task(task_id)
    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
        db.session.commit()
    except:
        abort(make_response(jsonify({"details":f"Invalid data"}), 400))
    return make_response(jsonify({"task": task.to_json()}),200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_a_task(task_id):
    task = fetch_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}), 200)