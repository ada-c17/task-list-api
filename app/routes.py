from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
import datetime
import requests

PATH = "https://slack.com/api/chat.postMessage"
SLACK_API_KEY = "xoxb-3491039968947-3488241064821-nC28KPl42UZ3B4XPMKax4yXn"

tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"details": f"{task_id} is not valid input."}
        abort(make_response(jsonify(response), 400))
    
    task = Task.query.get(task_id)

    if not task:
        response = {"details": f"Task {task_id} does not exist."}
        abort(make_response(jsonify(response), 404))
    
    return task

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })

    params = request.args
    if "sort" in params:
        if params["sort"] == "asc":
            response.sort(key=lambda x: x["title"])
            #response.order_by(Task.title)
        elif params["sort"] == "desc":
            response.sort(reverse=True, key=lambda x: x["title"])
    
    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }

    return jsonify(response), 200


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    
    try:
        if request_body.get("completed_at"):
            new_task = Task(title=request_body["title"],
                description=request_body["description"],
                completed_at=request_body["completed_at"])
                # When testing in Postman, make sure to add in format:
                # "2022-05-06"
        else:
            new_task = Task(title=request_body["title"],
                description=request_body["description"])
    except:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response), 400))
    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }
    }

    return jsonify(response), 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }

    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
    }
    return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_mark_complete(task_id):
    task = validate_task(task_id)

    # task.completed_at = datetime.date.today()
    # db.session.commit()

    if not task.completed_at:
        task.completed_at = datetime.date.today()
        db.session.commit()
        headers = {
            "Authorization": f"Bearer {SLACK_API_KEY}"
        }
        query_params = {
            "format": "json",
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}"
        }
        requests.get(PATH, headers=headers, params=query_params)


    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
        }
    }

    return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

    return jsonify(response), 200
