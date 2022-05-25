from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import os
import requests
from sqlalchemy.sql.functions import now
from .helper import validate_obj, sort_filter_get

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_tasks():
    new_task = Task.valid_task(request.get_json())

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.make_json()}), 201



@task_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = sort_filter_get(Task)

    tasks_response = [task.make_json() for task in tasks]        
    
    return make_response(jsonify(tasks_response),200)



@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_obj(Task,task_id)

    return make_response({"task" : task.make_json()}, 200)
    

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = validate_obj(Task,task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return make_response({'task':task.make_json()}, 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_a_task(task_id):
    task = validate_obj(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({'details':f'Task {task.task_id} "{task.title}" successfully deleted'},200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_obj(Task,task_id)
    
    task.completed_at = now()

    db.session.add(task)
    db.session.commit()
    if task.completed_at:
        requests.post("https://slack.com/api/chat.postMessage",
        data={
            "token": os.environ.get("SLACK_TOKEN"), 
            "channel": "task-notifications",
            "text": f"Task {task.title} has been completed."
            })
    return {
        "task": task.make_json()
    }, 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_obj(Task,task_id)

    task.completed_at = None

    db.session.add(task)
    db.session.commit()

    return {
        "task": task.make_json()
    }, 200
