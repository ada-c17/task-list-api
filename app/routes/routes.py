from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc,desc
import os
import requests
# from datetime import datetime
from sqlalchemy.sql.functions import now
# from .helper import validate_planet

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify(f"task {task_id} invalid"), 400))
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify(f"task {task_id} not found"), 404))
    return task

@task_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    if request_body['completed_at']:
        the_time = request_body['completed_at']
    else:
        the_time = None
    try:
        new_task = Task(title = request_body["title"], description = request_body["description"], completed_at = the_time)
        db.session.add(new_task)
        db.session.commit()
    except:
        abort(make_response({"details":f"Invalid data"}, 400))
    return make_response({"task" : new_task.make_json()}, 201)


@task_bp.route("", methods=["GET"])
def read_all_tasks():
    

    sort_query = request.args.get("sort")
    

    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()
    tasks_response = []    
    try:
        for task in tasks:
            tasks_response.append(task.make_json())
            
    except:
        abort(make_response({"details":f"task not found"}, 404))
    return make_response(jsonify(tasks_response),200)




@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    try:
        return make_response({"task" : task.make_json()}, 200)
    except:
        abort(make_response({"details":f"task {task_id} not found"}, 404))


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = validate_task(task_id)
    request_body = request.get_json()
    try: 
        task.title = request_body["title"]
        task.description = request_body["description"]
        
    except:
        abort(make_response(jsonify(f"task {task_id} not found"), 404))
    
    db.session.commit()

    return make_response({'task':task.make_json()}, 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_a_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({'details':f'Task {task.task_id} "{task.title}" successfully deleted'},200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return make_response({"details":"Invalid data"},404)
    
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
    task = Task.query.get(task_id)

    if not task:
        return make_response({"details":"Invalid data"},404)
    
    task.completed_at = None

    db.session.add(task)
    db.session.commit()

    return {
        "task": task.make_json()
    }, 200
