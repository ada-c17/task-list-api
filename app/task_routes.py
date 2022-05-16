import os
from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
# from sqlalchemy import desc
import requests

# import time
from datetime import date

from dotenv import load_dotenv
load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    
    return task



@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    #1st try
    try:
        request_body["completed_at"]
    except:
        request_body["completed_at"] = 0

    #2nd try
    try:
        request_body["description"]
        request_body["title"]
    except:
        return {"details": "Invalid data"}, 400

    #3rd try
    try:
        request_body["is_complete"]
    except:
        request_body["is_complete"] = False

    if request_body["completed_at"] != 0:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at= request_body["completed_at"],
                        is_complete=True)


        db.session.add(new_task)
        db.session.commit()

        return {
            "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": new_task.is_complete
            }
        }, 201
    
    new_task = Task.create_not_complete(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
        }
    }, 201
    


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_request = request.args.get("sort")
    title_query = request.args.get("title")

    tasks = Task.query.all()

    if sort_request == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    if sort_request == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    if title_query:
        tasks = Task.query.filter_by(title=title_query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
            }
        )
    return jsonify(tasks_response)



@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return {
        "task": {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    if task.completed_at:
        task.is_complete = True

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}



@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_is_complete(task_id):
    task = validate_task(task_id)

    task.is_complete = True
    task.completed_at = date.today() 
    
    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("SLACK_API_KEY")
    header = {"Authorization": API_KEY}
    query_params = {
        "channel": "task-notifications",
        "text": "Someone just completed the task"
    }

    requests.post(path, headers=header, params=query_params)

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }, 200



@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_is_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None 

    # db.session.add(task)
    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
    }, 200
