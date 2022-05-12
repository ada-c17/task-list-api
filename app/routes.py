from readline import parse_and_bind
from flask import Blueprint, make_response, request,jsonify, abort
from app import db
from app.models.task import Task
from datetime import datetime
import os
import requests
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

@task_bp.route("", methods=["GET"])
def get_all_saved_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
        #order_by function reference website
        #https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all() #list of objects
    tasks_response = []
    for task in tasks: #each row is converted to an object
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    response_body = {"task":
    {"id": task.id,
    "title": task.title,
    "description": task.description,
    "is_complete": bool(task.completed_at)
    }}
    
    if task.goal_id != None: #checking if task.goal_id is in the model Task, it is automatically None 
        response_body["task"]["goal_id"] = task.goal_id
    return jsonify(response_body)


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        response_body = {"details": "Invalid data"}
        return response_body, 400

    if "completed_at" not in request_body:
        new_task = Task(title = request_body["title"],
                description = request_body["description"])

    else:
        new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()
    response_body = {"task":
        {"id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": bool(new_task.completed_at)}
    }
    return jsonify(response_body), 201

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    
    response_body = {"task":
        {"id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }}
    return jsonify(response_body), 200

@task_bp.route("/<task_id>" , methods = ["DELETE"])
def delete_one_task(task_id):

    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response_body = (f'Task {task.id} "{task.title}" successfully deleted')

    return make_response(jsonify({"details":response_body}))

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def patch_task(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.now()
    query_params = {
        "channel": "task-notifications",
        "text": f'Someone just completed the task {task.title}'
    }
    header = {"Authorization": SLACK_BOT_TOKEN}

    url = 'https://slack.com/api/chat.postMessage'
    requests.post(url, params=query_params, headers=header)

    db.session.commit()
    
    response_body = {"task":
        {"id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }}
    return jsonify(response_body), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def patch_task_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    
    response_body = {"task":
        {"id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }}
    return jsonify(response_body), 200