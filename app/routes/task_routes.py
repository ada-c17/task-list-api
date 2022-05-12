from app import db
from flask import Blueprint, make_response, request
from ..models.task import Task
from .routes_helper import success_response, error_response, validate_item, post_completed_task_to_slack
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


#routes

@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body.get("completed_at")
            )
    except: 
        error_response({"details": "Invalid data"}, 400)

    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}

    return success_response(response_body, 201)
    # return make_response(jsonify(response_body), 201)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    
    sort_param = request.args.get("sort")

    if sort_param:
        if sort_param == "asc":
            tasks = Task.query.order_by(Task.title).all()
        elif sort_param == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    response_body = [task.to_dict() for task in tasks]

    return success_response(response_body, 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = validate_item(Task, task_id)

    response_body = {"task": task.to_dict()}

    return success_response(response_body, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task, task_id)
    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except KeyError as err:
        return make_response(f"Key error {err}", 400)
    
    db.session.commit()

    response_body = {"task": task.to_dict()}

    return success_response(response_body, 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    response_body = {"details": f'Task {task_id} "{task.title}" successfully deleted'}

    return success_response(response_body, 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_item(Task, task_id)
    task.completed_at = datetime.utcnow()
    
    db.session.commit()
    post_completed_task_to_slack(task.title)

    response_body = {"task": task.to_dict()}

    return success_response(response_body, 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_item(Task, task_id)
    task.completed_at = None
    
    db.session.commit()

    response_body = {"task": task.to_dict()}

    return success_response(response_body, 200)

