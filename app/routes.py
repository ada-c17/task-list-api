import datetime
from flask import Blueprint, request, jsonify, make_response, abort
import requests

from app.models.goal import Goal
from .models.task import Task
from app import db
import os

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_tasks():
    response_body = request.get_json()
    try:
        if response_body and "completed_at" in response_body:
            new_task = Task(title=response_body["title"], description=response_body["description"], completed_at=response_body["completed_at"])
        else:
            new_task = Task(title=response_body["title"], description=response_body["description"])
    except KeyError:
        return {
            "details": "Invalid data" #both title and description are required field
        }, 400 
    
    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task" : new_task.to_json()}, 201
    
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    """part of Wave02 sort by asc and desc"""
    params = request.args
    response_body, sort_cond = [], ""
    if "sort" in params:
        sort_cond = params["sort"]
        if sort_cond == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_cond == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    for task in tasks:
        response_body.append(
            task.to_json())
    
    return jsonify(response_body), 200

def id_validation(input_id):
    try:
        input_id = int(input_id)
    except ValueError:
        rsp = {"msg": f"Invalid task id #{input_id}."}
        abort(make_response(jsonify(rsp), 400))
    
    valid_id = Task.query.get(input_id)
     
    if valid_id is None:
        rsp = {"msg": f"Given task #{input_id} is not found."}
        #raise ValueError({"msg": f"Given task #{taskID} is not found."})
        abort(make_response(jsonify(rsp), 404))

    return valid_id

@task_bp.route("/<taskID>", methods=["GET"])
def get_one_task(taskID):
    task_exist = id_validation(taskID)
    
    return {
        "task": 
        task_exist.to_json() }, 200
    
"""date format for updating complete status works when input: 2021-05-30-07:19:06"""
@task_bp.route("/<taskID>", methods=["PUT"])
def update_task(taskID):
    task = id_validation(taskID)
    response_body = request.get_json()
    
    if response_body and "completed_at" in response_body:
        try:
            if isinstance(response_body["completed_at"], datetime.datetime):
                task.completed_at = response_body["completed_at"]
        except:
            raise ValueError("only supports date time in yy/mm/dd hh:mm:ss formats")  
        """ We don't have frontend UI for users, either we can build a calendar UI for the convenience or 
                we can also generate a documentation for developers who use this api, saying completed_at accepts a certain types of formats."""
    task.title = response_body["title"]
    task.description = response_body["description"]
    db.session.commit()
    
    #required in our test case, but response_body can be optional
    return {
        "task": task.to_json()}, 200
    
    
@task_bp.route("/<taskID>", methods=["DELETE"])
def delete_task(taskID):
    valid_task = id_validation(taskID)
    valid_task = Task.query.get(taskID)
    
    db.session.delete(valid_task)
    db.session.commit()
    
    return {"details": f'Task {valid_task.task_id} \"{valid_task.title}\" successfully deleted'
    }, 200
    
"""Wave03"""
"""Wave04"""

@task_bp.route("/<taskID>/mark_complete", methods=["PATCH"])
def update_tasks_with_completed(taskID):
    task = id_validation(taskID)
    task.completed_at = datetime.datetime.utcnow()
    db.session.commit()
    slack_api_call(task)  #bot message post
    
    return {
        "task": 
            task.to_json()}, 200

    

def slack_api_call(task):
    SLACK_PATH = "https://slack.com/api/chat.postMessage"
    OATH_TOKEN = os.environ.get("SLACK_TOKEN")
    HEADERS = {"Authorization": f"Bearer {OATH_TOKEN}"}
    PARAMS = {
        "channel": "task-notifications",
        "text": f"Completed the task {task.title}"
    }
    requests.post(SLACK_PATH, params=PARAMS, headers=HEADERS)
    
@task_bp.route("/<taskID>/mark_incomplete", methods=["PATCH"])
def update_tasks_with_not_completed(taskID):
    task = id_validation(taskID)

    task.completed_at = None
    db.session.commit()
    
    return { "task": task.to_json()}, 200
    
    
