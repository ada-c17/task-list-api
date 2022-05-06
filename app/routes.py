from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks_bp", __name__,  url_prefix="/tasks")
path="https://slack.com/api/chat.postMessage"
SLACK_API_KEY = os.environ.get("SLACK_AUTH_KEY")

@tasks_bp.route("about", methods=["GET"])
def about():
    return "The Task List Project by: Nina Patrina. Ada Developers Academy, 2022"

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"task {id} invalid"}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"message":f"task {id} not found"}, 404))

    return task

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    except KeyError:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        new_task.completed_at =request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    return { 
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }}, 201

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    params = request.args
    if "sort" in params:
        tasks = Task.query.order_by(Task.title.asc()) if params["sort"]=="asc" else Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return  { 
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return { 
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}, 200

@tasks_bp.route("/<task_id>/<mark>", methods=["PATCH"])
def update_task1(task_id, mark):
    task = validate_task(task_id)

    if mark =="mark_complete":
        task.completed_at =datetime.utcnow() 
        slack_headers =  {"Authorization" :SLACK_API_KEY}
        myobj={"channel" :"task-notifications",
               "text":f"Someone just completed the task {task.title}"}
        requests.post(path,data = myobj, headers=slack_headers)

    elif mark =="mark_incomplete": 
        task.completed_at =None

    db.session.commit()

    return { 
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}