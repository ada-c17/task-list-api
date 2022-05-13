from app import db
from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from datetime import datetime
from dotenv import load_dotenv
import os, requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"msg":f"Invalid task id: {task_id}. ID must be an integer."}
        return response, 400

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        new_task = Task(title=request_body["title"], 
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
    else:
        new_task = Task(title=request_body["title"], 
                description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response = new_task.create_task_dict()
    return response, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_sort_query = request.args.get("sort")
    if title_sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append(task.create_simple_task_dict())

    return jsonify(response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    requested_task = Task.query.get(task_id)

    if requested_task is None:
        return {"msg":f"Could not find task with id: {task_id}"}, 404
    
    response = requested_task.create_task_dict()
    return response

@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    requested_task = Task.query.get(task_id)
    if requested_task is None:
        return {"msg":f"Could not find task with id: {task_id}"}, 404

    requested_task.title = request_body["title"]
    requested_task.description = request_body["description"]

    db.session.commit()

    response = requested_task.create_task_dict()
    return response

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    requested_task = Task.query.get(task_id)
    if requested_task is None:
        response = {"msg":f"Could not find task with id: {task_id}"}
        return response, 404

    db.session.delete(requested_task)
    db.session.commit()

    response = {"details": f'Task {requested_task.task_id} "{requested_task.title}" successfully deleted'}

    return response

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_task(task_id)

    requested_task = Task.query.get(task_id)
    if requested_task is None:
        response = {"msg":f"Could not find task with id: {task_id}"}
        return response, 404
    
    requested_task.completed_at = datetime.now()

    db.session.commit()

    response = requested_task.create_task_dict()

    path = "https://slack.com/api/chat.postMessage"
    data = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {requested_task.title}"
    }
    headers = {
        "authorization": "Bearer " + os.environ.get("SLACKBOT_API_KEY")
    }

    post_message = requests.post(path, data=data, headers=headers)
    
    return response

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_task(task_id)

    requested_task = Task.query.get(task_id)
    if requested_task is None:
        response = {"msg":f"Could not find task with id: {task_id}"}
        return response, 404
    
    requested_task.completed_at = None


    db.session.commit()

    response = requested_task.create_task_dict()
    return response
