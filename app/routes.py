import datetime
from flask import Blueprint, request, jsonify, make_response, abort
import requests
from .models.task import Task
from app import db
import os

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def completed_or_not(response_body):
    # [response] iterage in list of object, otherwise, TypeError
    if response_body and "completed_at" in [response_body]:
        completed_status = True
    else:
        completed_status = False
    return completed_status

@task_bp.route("", methods=["POST"])
def create_tasks():
    response_body = request.get_json()
    completed_status = False
    try:
        if response_body and "completed_at" in response_body:
            completed_status = True
            new_task = Task(title=response_body["title"], description=response_body["description"], completed_at=datetime.datetime.utcnow())
        else:
            completed_status = False
            new_task = Task(title=response_body["title"], description=response_body["description"])
    except KeyError:
        return {
            "details": "Invalid data" #both title and description are required field
        }, 400 
    
    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": completed_status
    }}, 201

    #completed_status = completed_or_not(response_body)
    #print(completed_status)
    # try:
    #     if completed_status == True:
    #         print("pass?")
    #          #completed_status = True
    #         new_task = Task(title=response_body["title"], description=response_body["description"], completed_at=datetime.datetime.utcnow())
    #     else:
    #          #completed_status = False
    #         new_task = Task(title=response_body["title"], description=response_body["description"])
    # except KeyError:
    #      return {
    #          "details": "Invalid data" #both title and description are required field
    #      }, 400 
    
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
    
    completed_status = completed_or_not(tasks)   
    for task in tasks:
        response_body.append({
            "id": task.task_id, 
            "title":task.title, 
            "description": task.description,
            "is_complete": completed_status
        })
    
    return jsonify(response_body), 200

def task_validation(taskID):
    try:
        taskID = int(taskID)
    except ValueError:
        rsp = {"msg": f"Invalid task id #{taskID}."}
        abort(make_response(jsonify(rsp), 400))
    
    valid_task = Task.query.get(taskID)
    
    if valid_task is None:
        rsp = {"msg": f"Given task #{taskID} is not found."}
        #raise ValueError({"msg": f"Given task #{taskID} is not found."})
        abort(make_response(jsonify(rsp), 404))

    return valid_task

@task_bp.route("/<taskID>", methods=["GET"])
def get_one_task(taskID):
    task_exist = task_validation(taskID)
    completed_status = completed_or_not(task_exist)

    rsp = {
        "task": {
        "id": task_exist.task_id,
        "title": task_exist.title,
        "description": task_exist.description,
        "is_complete": completed_status
    }}
    return jsonify(rsp), 200

@task_bp.route("/<taskID>", methods=["PUT"])
def update_task(taskID):
    task = task_validation(taskID)
    response_body = request.get_json()
    #completed_status = completed_or_not(response_body)
    if response_body and "completed_at" in response_body:
        #update this task_id's title and description. *Forgot assign task_id*
        task.completed_at = datetime.datetime.utcnow()
        completed_status = True
    else:
        completed_status = False
        
    task.title = response_body["title"]
    task.description = response_body["description"]
    
    #required in our test case, but response_body can be optional
    rsp = {
        "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": completed_status
    }}

    db.session.commit()
    
    return jsonify(rsp), 200
    
    
@task_bp.route("/<taskID>", methods=["DELETE"])
def delete_task(taskID):
    valid_task = task_validation(taskID)
    valid_task = Task.query.get(taskID)
    
    db.session.delete(valid_task)
    db.session.commit()
    
    return {"details": f'Task {valid_task.task_id} \"{valid_task.title}\" successfully deleted'
    }, 200
    
"""Wave03"""
@task_bp.route("/<taskID>/mark_complete", methods=["PATCH"])
def update_tasks_with_completed(taskID):
    task = task_validation(taskID)
    task.completed_at = datetime.datetime.utcnow()
    #db.session.add(task)
    db.session.commit()
    #bot message post
    slack_api_call(task)
    
    return {
        "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": True
    }}, 200

    
    
@task_bp.route("/<taskID>/mark_incomplete", methods=["PATCH"])
def update_tasks_with_not_completed(taskID):
    task = task_validation(taskID)

    task.completed_at = None
    db.session.commit()
    
    return {
        "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
    }}, 200
    
"""Wave04"""
def slack_api_call(task):
    SLACK_PATH = "https://slack.com/api/chat.postMessage"
    OATH_TOKEN = os.environ.get("SLACK_TOKEN")
    HEADERS = {"Authorization": f"Bearer {OATH_TOKEN}"}
    PARAMS = {
    "channel": "task-notifications",
    "text": "Completed the task {task.title}"
    }
    response = requests.post(SLACK_PATH, params=PARAMS, headers=HEADERS)
