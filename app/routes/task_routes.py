from datetime import datetime
import requests
import os

from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


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

    return {"task": Task.task_response(new_task)}, 201


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
        tasks_response.append(Task.task_response(task))
        if task.goal_id:
            tasks_response.append({"goal_id": task.goal_id})

    return jsonify(tasks_response)


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    '''Request information about a specific Task.'''
    task = Task.validate_task(task_id)
    response_body = Task.task_response(task)
    if task.goal_id:
        response_body["goal_id"] = task.goal_id
    return {"task": response_body}


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    '''Update a Task record. Title and description are required.'''
    task = Task.validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    if task.completed_at:
        task.completed_at = request_body["completed_at"]
    
    db.session.commit()
    
    return {"task": Task.task_response(task)}


def send_slack_notice(title):
    '''Posts a notification on Slack everytime a task is marked completed'''
    PATH = os.environ.get("SLACK_PATH")
    auth_header = {"Authorization":f"Bearer {os.environ.get('SLACK_TOKEN')}"}
    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {title}"
    }

    slack_post = requests.post(PATH, params=query_params, headers=auth_header)

    return slack_post


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    '''Marks a Task as complete. Requires DateTime for completed_at.'''
    task = Task.validate_task(task_id)
    task.completed_at = datetime.utcnow()
    
    db.session.commit()

    send_slack_notice(task.title)

    return {"task": Task.task_response(task)}


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    '''Marks a Task as incomplete.'''
    task = Task.validate_task(task_id)
    task.completed_at = None
    
    db.session.commit()
    
    return {"task": Task.task_response(task)}


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    '''Deletes a Task. Can not be undone.'''
    task = Task.validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}
