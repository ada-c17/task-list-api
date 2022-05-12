from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app import db
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    '''Validates that task id is valid and exists'''
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"msg": f"Invalid id: {task_id}"}, 400))
    
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"msg": f"Could not find task with id: {task_id}"}, 404))
    return task

def is_complete(task):
    '''Checks whether a task is incomplete or complete.'''
    if task.completed_at:
        return True
    else:
        return False

def send_slack_notice(title):
    '''Posts a notification on Slack everytime a task is marked completed'''
    PATH = os.environ.get("SLACK_PATH")
    AUTH_HEADER = {"Authorization":f"Bearer {os.environ.get('SLACK_TOKEN')}"}
    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {title}"
    }
    slack_post = requests.post(PATH, params=query_params, headers=AUTH_HEADER)
    return slack_post

@task_bp.route("", methods=["POST"])
def create_task():
    '''Creates a new Task record. Entering a date for "completed_at" is optional.'''
    request_body = request.get_json()
    try:
        new_task = Task(
            title=request_body["title"], 
            description=request_body["description"],
            completed_at=request_body["completed_at"]
            )
    except KeyError:
        try:
            new_task = Task(
                title=request_body["title"], 
                description=request_body["description"],
                )
        except KeyError:
            return {"details": "Invalid data"}, 400

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete(new_task)
        }
    }, 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    '''Returns all Tasks. Default sorted by id, but can be sorted asc/desc by title.'''
    task_query = request.args
    
    if task_query and task_query["sort"] == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif task_query and task_query["sort"] == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete(task)
        })
        if task.goal_id:
            tasks_response.append({
                "goal_id": task.goal_id
                })
    return jsonify(tasks_response)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    '''Request information about a specific Task.'''
    task = validate_task(task_id)

    response_body = {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete(task)
        }
    if task.goal_id:
        response_body["goal_id"] = task.goal_id

    return { 
        "task": response_body
    }

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    '''Update a Task record. Title and description are required.'''
    task = validate_task(task_id)
    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]
    except KeyError:
        task.title = request_body["title"]
        task.description = request_body["description"]
    
    db.session.commit()
    
    return { 
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete(task)
        }
    }

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    '''Marks a Task as complete. Requires DateTime for completed_at.'''
    task = validate_task(task_id)
    task.completed_at = datetime.utcnow()
    
    db.session.commit()

    send_slack_notice(task.title)

    return { 
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete(task)
        }
    }

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    '''Marks a Task as incomplete.'''
    task = validate_task(task_id)
    task.completed_at = None
    
    db.session.commit()
    
    return { 
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete(task)
        }
    }

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    '''Deletes a Task. Can not be undone.'''
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}
