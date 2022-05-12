import json
from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app import db
from datetime import datetime
import os, requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#view all tasks
@tasks_bp.route("", methods=["GET"])
def view_tasks():
    title_query = request.args.get("sort")
    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_json())
        
    return jsonify(tasks_response), 200


#view one task
@tasks_bp.route("/<int:id>", methods=["GET"])
def view_task(id):
    task = validate_task(id)

    return jsonify({"task": task.to_json()}), 200


#create a task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        if "completed_at" in request_body:
            new_task = Task(title = request_body["title"],
            description = request_body["description"], completed_at = request_body["completed_at"])

        else:
            new_task = Task(title = request_body["title"],
            description = request_body["description"])

    except KeyError:
        return make_response({"details": "Invalid data"},400)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_json()}), 201


#delete a task
@tasks_bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {id} "{task.to_json()["title"]}" successfully deleted'}), 200


#update a task
@tasks_bp.route("/<int:id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task.to_json()}), 200


#mark task complete
@tasks_bp.route("/<int:id>/mark_complete", methods=["PATCH"])
def complete_task(id):
    task = validate_task(id)
    request_body = request.get_json()

    task.completed_at = datetime.now()

    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"
    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    
    headers = {"Authorization": os.environ.get("SLACK_BOT_KEY")}
    response_bot = requests.post(path, params=query_params, headers=headers)
    return jsonify({"task":task.to_json()}), 200


#mark task incomplete
@tasks_bp.route("/<int:id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(id):
    task = validate_task(id)
    request_body = request.get_json()

    task.completed_at = None

    db.session.commit()

    return jsonify({"task":task.to_json()}), 200


def validate_task(id):
    try:
        id = int(id)
    except:
        return abort(make_response({"message": f"Task {id} is invalid"}, 400))

    task = Task.query.get(id)

    if not task:
        return abort(make_response({"message": f"Task {id} not found"}, 404))
    
    return task


