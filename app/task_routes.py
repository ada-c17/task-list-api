from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# helper functions
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"error": f"Task id invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"error":f"Task not found"}, 404))
    return task

def slack_bot(task):
    load_dotenv()
    message = f"Someone just completed the task {task.title}"
    slack_url = "https://slack.com/api/chat.postMessage"
    header = {'Authorization': f'Bearer {os.environ.get("SLACK_API_TOKEN")}'}
    param = {"channel": "task-notifications", 
        "text": message}

    return requests.post(url=slack_url, params=param, headers=header)

# creates new task to the database
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    
    if "completed_at" in request_body:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"])
    else:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": new_task.make_dict()
    }
    return make_response(jsonify(response_body), 201)


# get all saved tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query  = request.args.get("title")
    description_query = request.args.get("description")
    sort_query = request.args.get("sort")

    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif description_query:
        tasks = Task.query.filter_by(description=description_query)
    else:
        tasks = Task.query.all()

    response_body = [task.make_dict() for task in tasks]
    return make_response(jsonify(response_body), 200)


# get one task by task id 
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    response_body = {
        "task": task.make_dict()}
    return make_response(jsonify(response_body), 200)


# update a task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_body = {
        "task": task.make_dict()
    }
    return make_response(jsonify(response_body), 200)

# delete a task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details":f'Task {task.task_id} "{task.title}" successfully deleted'}
    return make_response(jsonify(response_body), 200)


# patches a task to mark as complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_as_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.utcnow()

    db.session.commit()
    slack_bot(task)

    response_body = {
        "task": task.make_dict()}
    return make_response(jsonify(response_body), 200)


# patches a task to mark as incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_as_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None

    db.session.commit()

    response_body = {
        "task": task.make_dict()}
    return make_response(jsonify(response_body), 200)