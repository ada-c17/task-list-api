from flask import Blueprint, request, jsonify, make_response
from app.models.task import Task
from app import db 
from sqlalchemy import desc, asc
from datetime import datetime 
import requests
import os  

PATH = "https://slack.com/api/chat.postMessage?channel=task-notifications&text="

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        return {"details": "Invalid data"}, 400

    # before refactoring
    # if "description" not in request_body or "title" not in request_body:
    #     return {"details": "Invalid data"}, 400

    # if "completed_at" in request_body:
    #     new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
    # else:
    #     new_task = Task(title=request_body["title"], description=request_body["description"])

    new_task = Task.from_json(request_body)
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_json()
    }, 201


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.validate_task(task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()
    
    headers = { "Authorization": "Bearer " + os.environ.get("SLACK_API_TOKEN", "") }
    
    requests.post(PATH + f"Someone just completed the task {task.title}", headers=headers)

    return {
        "task": task.to_json()
    }, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    return {
        "task": task.to_json()
    }, 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.validate_task(task_id)
    response = {
            "task": task.to_json()
        }

    if task.goal_id:
        response["task"]["goal_id"] = task.goal_id
        
    return make_response(jsonify(response)), 200


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args 
    if "sort" in params:
        sort = params["sort"]
        if sort.lower() == "asc":
            tasks = Task.query.order_by(asc(Task.title)).all()
        elif sort.lower() == "desc":
            tasks = Task.query.order_by(desc(Task.title)).all()
        elif sort.lower() == "id-asc":
            tasks = Task.query.order_by(asc(Task.task_id)).all()
        elif sort.lower() == "id-desc":
            tasks = Task.query.order_by(desc(Task.task_id)).all()
    else:    
        tasks = Task.query.all()

    if "title" in params:
        title = params["title"]
        tasks = Task.query.filter_by(title=title)
    
    # before refactoring
    # tasks_response = []

    # if len(tasks) == 0:
    #     return jsonify(tasks_response), 200

    # for task in tasks:
    #     tasks_response.append(task.to_json())

    tasks_response = [task.to_json() for task in tasks]
    
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.validate_task(task_id)
    request_body = request.get_json()

    if "title" and "description" in request_body:
        task.title = request_body["title"]
        task.description = request_body["description"]
    else: 
        return {"details": "Invalid data"}, 400

    db.session.commit()

    return {
        "task": task.to_json()
    }, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }), 200