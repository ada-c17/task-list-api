import os
from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime, timezone
import requests 
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('PROJECT_API_KEY')

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
homepage_bp = Blueprint("homepage_bp", __name__, url_prefix="/")

@homepage_bp.route("", methods=["GET"])
def welcome():
    """Greets visitors"""
    return jsonify({"Welcome!": "Here is my task list API :)"}), 200

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    """Displays all tasks"""
    response_body = []

    # Get sort query. If sort query, sort according to param. If not, get all tasks unsorted.
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    # Convert all tasks into dictionaries and display them
    for task in tasks: 
        task_dict = task.make_task_dict()
        response_body.append(task_dict)
        
    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    """Displays one task when given a task id"""
    task = Task.validate_task(task_id)
    task_dict = {"task": task.make_task_dict()}
    return jsonify(task_dict), 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    """Creates one task"""
    request_body = request.get_json()
    
    # Tries to create a task with given request body. Throws an error if needed data is missing.
    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"])
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    task_dict = {"task": new_task.make_task_dict()}

    return jsonify(task_dict), 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updates the data stored in a task with a given task id"""
    task = Task.validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]

    db.session.commit()

    task_dict = {"task": task.make_task_dict()}

    return jsonify(task_dict), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletes a task with a given task id"""
    task = Task.validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    """Marks a task as complete with a given task id"""
    task = Task.validate_task(task_id)
    # Check if task is incomplete. If it is, mark it as completed at the current time.
    if task.completed_at == None:
        task.completed_at = datetime.now()
        task.completed_at = task.completed_at.replace(tzinfo=timezone.utc)
    
    task_dict = {"task": task.make_task_dict()}

    db.session.commit()

    # Make a request to slackbot API
    payload = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task_dict['task']['title']}"
        }
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    bot_request = requests.post("https://slack.com/api/chat.postMessage", headers=headers, params=payload)

    return jsonify(task_dict), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    """Mark a task as incomplete with a give task id"""
    task = Task.validate_task(task_id)
    if task.completed_at != None:
        task.completed_at = None

    task_dict = {"task": task.make_task_dict()}

    db.session.commit()

    return jsonify(task_dict), 200
    




