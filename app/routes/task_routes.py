from app import db
from app.routes.helper import validate_task, slack_bot
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request
# import requests
# import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# GET ALL TASKS - "/tasks" - GET
@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    # SORT
    sort = request.args.get("sort")
    if sort == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = [task.t_json() for task in tasks]

    return jsonify(tasks_response), 200


# GET ONE TASK
@tasks_bp.route("/<id>", methods = ["GET"])
def get_one_task(id):
    task = validate_task(id)
    return jsonify({"task":task.t_json()}), 200


# CREATE TASK
@tasks_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()
    try:
        new_task = Task.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.t_json()}), 201


# UPDATE ONE TASK - "/tasks/1" - PUT
@tasks_bp.route("/<id>", methods = ["PUT"])
def update_task(id):
    task = validate_task(id) # can i make this a global variable?
    request_body = request.get_json()
    task.update(request_body)

    db.session.commit()

    return jsonify({"task":task.t_json()}), 200


# DELETE - "/tasks/1" - DELETE
@tasks_bp.route("/<id>", methods = ["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()
        
    return jsonify({"details":f'Task {id} "{task.t_json()["title"]}" successfully deleted'}), 200


# MARKED COMPLETED (SEND TO SLACK) - "/tasks/1/mark_complete" - PATCH
@tasks_bp.route("/<id>/mark_complete", methods = ["PATCH"])
def mark_completed(id):
    task = validate_task(id) # can i make this a global variable?
    task.patch_complete()

    db.session.commit()

    slack_bot(task)

    return jsonify({"task":task.t_json()}), 200


# MARK INCOMPLETE - "/tasks/1/mark_incomplete" - PATCH
@tasks_bp.route("/<id>/mark_incomplete", methods = ["PATCH"])
def mark_imcompleted(id):
    task = validate_task(id)
    task.patch_imcomplete()

    db.session.commit()

    return jsonify({"task":task.t_json()}), 200

