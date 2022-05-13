from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

PATH = "https://slack.com/api/chat.postMessage"
API_KEY = os.environ.get("SLACK_TOKEN")


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

def validate_input(item_id, model_name):
    try:
        item_id = int(item_id)
    except ValueError:
        response = {"msg": f"Invalid id: {item_id}"}
        abort(make_response(jsonify(response), 400))

    chosen_item = model_name.query.get(item_id)    

    if chosen_item is None:
        response = {"msg": f"Could not find item with id {item_id}"}
        abort(make_response(jsonify(response), 404))
    return chosen_item

def task_body(task):
    return {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }

def create_task_dictionary(chosen_task):
    task_dict= {}
    task_dict["task"] = task_body(chosen_task)
    if chosen_task.goal_id:
            task_dict["task"].update({"goal_id": chosen_task.goal_id})

    return task_dict

def create_slack_api_request(chosen_task):
    params = {
        "text": f"Someone just completed the task {chosen_task.title}",
        "channel": "task-notifications"
        }
    hdrs = {
        "Authorization": f"Bearer {API_KEY}"
    }
    r = requests.post(PATH, data = params, headers = hdrs)
    return r

@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    params = request.args
    if params and params["sort"] == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif params and params["sort"] == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()
    task_response = [task_body(task) for task in tasks]

    return jsonify(task_response), 200

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    chosen_task = validate_input(task_id, Task)
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200

@tasks_bp.route("", methods = ["POST"])
def create_one_task():
    request_body = request.get_json()

    try:
        if request_body.get("completed_at"):
            chosen_task = Task( title = request_body["title"],
                        description = request_body["description"],
                        completed_at = request_body["completed_at"]
                        )
        else:
            chosen_task = Task( title = request_body["title"],
                        description = request_body["description"]
                        )
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(chosen_task)
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 201

@tasks_bp.route("/<task_id>", methods = ["PUT"])
def add_one_task(task_id):
    chosen_task = validate_input(task_id, Task)
    request_body = request.get_json()
    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
    except KeyError:
        return {
            "msg": "title and description are required"
        }, 400
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    chosen_task = validate_input(task_id, Task)
    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{chosen_task.title}" successfully deleted'
    }, 200

@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def update_task_complete(task_id):
    chosen_task = validate_input(task_id, Task)
    chosen_task.completed_at = datetime.utcnow()
    create_slack_api_request(chosen_task)
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def update_task_incomplete(task_id):
    chosen_task = validate_input(task_id, Task)
    chosen_task.completed_at = None
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200

