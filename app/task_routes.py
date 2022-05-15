from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from .route_helpers import fetch_type, slack_post
from sqlalchemy import asc, desc
from datetime import date

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
####################
#POST creates a task
#json:title, decription, completed_at(if already complete)
#returns created task
####################
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    completed_at = None
    if "completed_at" in request_body:
        completed_at = request_body["completed_at"]
    try:
        new_task = Task(title = request_body["title"], description = request_body["description"], completed_at = completed_at)
        db.session.add(new_task)
        db.session.commit()
    except:
        abort(make_response(jsonify({"details":f"Invalid data"}), 400))
    return make_response(jsonify({"task": new_task.to_json()}), 201)

####################
#GET gets all tasks with optional sort ascending or descending
#returns list of all tasks
####################
@task_bp.route("", methods=["GET"])
def fetch_all_tasks():

    sort = request.args.get("sort")
    if sort == "asc":
        tasks = Task.query.filter_by().order_by(Task.title.asc())
    elif sort == "desc":
        tasks = Task.query.filter_by().order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    task_response = [task.to_json() for task in tasks]
    return make_response(jsonify(task_response),200)

####################
#GET gets a task
#route /task_id
#returns created task
####################
@task_bp.route("/<task_id>", methods=["GET"])
def fetch_a_task(task_id):
    task = fetch_type("task", task_id)
    return make_response(jsonify({"task": task.to_json()}), 200)

####################
#PUT updates a task
#route /<task_id>
#json: title, description, completed_at(optional)
#returns created task
####################
@task_bp.route("/<task_id>", methods=["PUT"])
def update_a_task(task_id):
    
    task = fetch_type("task", task_id)
    request_body = request.get_json()
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
        db.session.commit()
    except:
        abort(make_response(jsonify({"details":f"Invalid data"}), 400))
    return make_response(jsonify({"task": task.to_json()}),200)

####################
#DELETE deletes a task
#route /<task_id>
#returns message that task was deleted
####################
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_a_task(task_id):
    task = fetch_type("task", task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}), 200)

####################
#PATCH updates a task as complete or incomplete
#route /<task_id>/mark_incomplete or /<task_id>/mark_complete
#returns updated task info
####################
@task_bp.route("/<task_id>/mark_<status>", methods=["PATCH"])
def update_task_complete(task_id, status):
    
    task = fetch_type("task", task_id)

    if status == "complete":
        task.completed_at = date.today()
        slack_post(task.title)


    elif status == "incomplete":
        task.completed_at = None
    else:
        abort(make_response(jsonify({"details":f"Invalid endpoint"}), 400))

    db.session.commit()
    return make_response(jsonify({"task": task.to_json()}),200)