from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from sqlalchemy import desc, func
import requests
import os

task_bp = Blueprint("tasks", __name__ , url_prefix="/tasks")

def validate_task(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        abort(make_response(jsonify(f"Task {task_id} not found"), 404))

    return task
  
@task_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_param_value = request.args.get("sort")
    tasks = []

    if sort_param_value is None:
        tasks = Task.query.all()
    elif sort_param_value == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_param_value == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return jsonify({"task": task.to_dict()}), 200

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if request_body is None or not "title" in request_body or not "description" in request_body:
        return jsonify({"details": "Invalid data"}), 400
         
    completed_at = None
    if "completed_at" in request_body:
        completed_at = request_body["completed_at"]

    new_task = Task(title=request_body["title"], 
                    description=request_body["description"], 
                    completed_at=completed_at)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200 

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }

    return jsonify(response), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def completed_task(task_id):
    task = validate_task(task_id)

    task.completed_at = func.now()
    db.session.commit()

    text = f"Someone just completed the task {task.title}"
    url = os.environ.get("URL")
    json = {
        "channel": "task-notification",
        "text": text
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.environ.get("AUTHORIZATION")
    }
    requests.post(url, json=json, headers=headers)

    return jsonify({"task": task.to_dict()}), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incompleted_task(task_id):
    task = validate_task(task_id)

    if not task.completed_at is None:
        task.completed_at = None
        db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


    
    





    