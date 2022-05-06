from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy import asc,desc
from datetime import datetime, date

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

# helper function to validate
def validate_task(id):
    try:
        task_id = int(id)
    except:
        return abort(make_response(jsonify("Task is invalid"), 400))

    task = Task.query.get(task_id)

    if not task:
        return abort(make_response(jsonify(f"Task {id} does not exist"), 404))
    return task

# Get all tasks
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all() 

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id":task.id,
            "title":task.title,
            "description":task.description,
            "is_complete": True if task.completed_at else False
            })
    return make_response(jsonify(tasks_response), 200)

# Get one task
@task_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)
    response_body = {}

    response_body["task"] = {
        "id":task.id,
        "title":task.title,
        "description":task.description,
        "is_complete": True if task.completed_at else False
        }
    
    return make_response(jsonify(response_body), 200)

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        if 'completed_at' in request_body:
            new_task = Task(
                title=request_body["title"],
                description=request_body["description"],
                completed_at=request_body["completed_at"])
        else:
            new_task = Task(
                title=request_body["title"],
                description=request_body["description"])
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.add(new_task)
    db.session.commit()

    response_body = {}
    response_body["task"] = {
            "id":new_task.id,
            "title":new_task.title,
            "description":new_task.description,
            "is_complete": True if new_task.completed_at else False
            }

    return make_response(jsonify(response_body), 201)

@task_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json()

    try:
        if 'completed_at' in request_body:
            task.title = request_body["title"]
            task.description = request_body["description"]
            task.completed_at = request_body["completed_at"]
        else:
            task.title = request_body["title"]
            task.description = request_body["description"]
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.commit()
    
    response_body = {}
    response_body["task"] = {
            "id":task.id,
            "title":task.title,
            "description":task.description,
            "is_complete": True if task.completed_at else False
            }
    
    return make_response(jsonify(response_body), 200)

# PATCH REQUEST - MARK COMPLETE
@task_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_task(id)

    task.completed_at = date.today()

    db.session.commit()

    response_body = {}
    response_body["task"] = {
            "id":task.id,
            "title":task.title,
            "description":task.description,
            "is_complete": True if task.completed_at else False
            }
    
    return make_response(jsonify(response_body), 200)

# PATCH REQUEST - MARK INCOMPLETE
@task_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_task(id)

    task.completed_at = None

    db.session.commit()

    response_body = {}
    response_body["task"] = {
            "id":task.id,
            "title":task.title,
            "description":task.description,
            "is_complete": True if task.completed_at else False
            }
    
    return make_response(jsonify(response_body), 200)

# DELETE
@task_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({'details':f'Task {task.id} \"{task.title}\" successfully deleted'}), 200)