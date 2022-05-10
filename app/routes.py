import datetime
from flask import Blueprint, request, jsonify, make_response, abort
import requests

from app.models.goal import Goal
from .models.task import Task
from app import db
import os

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

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
    task = id_validation(taskID)
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
    task = id_validation(taskID)

    task.completed_at = None
    db.session.commit()
    
    return {
        "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
    }}, 200
    

def slack_api_call(task):
    SLACK_PATH = "https://slack.com/api/chat.postMessage"
    OATH_TOKEN = os.environ.get("SLACK_TOKEN")
    HEADERS = {"Authorization": f"Bearer {OATH_TOKEN}"}
    PARAMS = {
        "channel": "task-notifications",
        "text": f"Completed the task {task.title}"
    }
    requests.post(SLACK_PATH, params=PARAMS, headers=HEADERS)
    
    
"""Wave05"""
@goal_bp.route("", methods=["POST"])
def create_goals():
    resquest_body = request.get_json()
    
    if "title" in resquest_body:
        goal = Goal(title=resquest_body["title"])
    else:
        return {"details": "Invalid data"}, 400
    
    db.session.add(goal)
    db.session.commit()
    
    return {
        "goal":
            {
            "id": goal.goal_id,
            "title": goal.title
            }
    }, 201
    
@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    response_body = []
    for goal in goals:
        response_body.append({
            "id": goal.goal_id,
            "title": goal.title    
        })
    
    return jsonify(response_body), 200


def goal_id_validation(input_id):
    try:
        input_id = int(input_id)
    except ValueError:
        rsp = {"msg": f"Invalid task id #{input_id}."}
        abort(make_response(jsonify(rsp), 400))
    
    valid_id = Goal.query.get(input_id)
     
    if valid_id is None:
        rsp = {"msg": f"Given task #{input_id} is not found."}
        #raise ValueError({"msg": f"Given task #{taskID} is not found."})
        abort(make_response(jsonify(rsp), 404))

    return valid_id

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = goal_id_validation(goal_id)
    
    rsp = {
    "goal": {
        "id": goal.goal_id,
        "title": goal.title,
    }}
    return jsonify(rsp), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = goal_id_validation(goal_id)
    request_body = request.get_json()
    
    if request_body and "title" in request_body:
        goal.title = request_body["title"]
    db.session.commit()
    
    return jsonify({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }), 200
    
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = goal_id_validation(goal_id)
    goals = Goal.query.all()
    
    if len(goals) < 1:
        raise AttributeError("No object!")
    
    db.session.delete(goal)
    db.session.commit()
    
    return {
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
    }, 200