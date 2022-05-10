import datetime
import json
from flask import Blueprint, request, jsonify, make_response, abort
import requests

from app.models.goal import Goal
from .models.task import Task
from app import db
import os

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

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

@task_bp.route("/<taskID>", methods=["PUT"])
def update_task(taskID):
    task = id_validation(taskID)
    response_body = request.get_json()
    if response_body and "completed_at" in response_body:
        #update this task_id's title and description. *Forgot assign task_id*
        task.completed_at = response_body["completed_at"]
        
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
        response_body.append(goal.to_json())
    
    return jsonify(response_body), 200


def goal_id_validation(input_id):
    try:
        input_id = int(input_id)
    except ValueError:
        rsp = {"msg": f"Invalid goal id #{input_id}."}
        abort(make_response(jsonify(rsp), 400))
    
    valid_id = Goal.query.get(input_id)
     
    if valid_id is None:
        rsp = {"msg": f"Given goal #{input_id} is not found."}
        #raise ValueError({"msg": f"Given task #{taskID} is not found."})
        abort(make_response(jsonify(rsp), 404))

    return valid_id

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = goal_id_validation(goal_id)
    
    return jsonify({
         "goal": goal.to_json()}), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = goal_id_validation(goal_id)
    request_body = request.get_json()
    
    if request_body and "title" in request_body:
        goal.title = request_body["title"]
    db.session.commit()
    
    return jsonify({
        "goal": goal.to_json()
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
    
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_for_one_goal(goal_id):
    goal = goal_id_validation(goal_id)
    goal = Goal.query.get(goal_id) 
    #goal.tasks [] empty at this point
    
    request_body = request.get_json()
    #"task_ids": [1, 2, 3]
    #each Goal has (zero)one or many tasks[]
    for task_id in request_body.get("task_ids"):
        #build relationship between goal and task here
        task = Task.query.get(task_id)
        goal.tasks.append(task)
    
    #db.session.add(task)
    db.session.commit()
    #goal.tasks = [<Task1>, <Task 2>, <Task 3>]
    
    return jsonify({
        "id": task.goal_id,
        "task_ids": request_body.get("task_ids")
    }), 200
"""
database visualization
 task_id |       title        |           description            |        completed_at        | goal_id 
---------+--------------------+----------------------------------+----------------------------+---------
       3 | A Brand New Task   | Test Description                 |                            |        
       6 | A Brand New Task   | Test Description                 |                            |        
       7 | A Brand New Task   | Test Description                 |                            |        
       9 | A Brand New Task   | Test Description                 |                            |        
      10 | A Brand New Task   | Test Description                 |                            |        
      12 | Coding flask       | Due next Friday                  |                            |        
      13 | Capstone Project   | Build full stack web application |                            |        
      11 | Updated Task Title | Updated Test Description         | 2022-05-07 03:21:52.90605  |        
       4 | A Brand New Task   | Test Description                 | 2022-05-07 20:51:40.542297 |        
       5 | A Brand New Task   | Test Description                 | 2022-05-07 20:51:58.383394 |        
       2 | A Brand New Task   | Test Description                 | 2022-05-07 21:05:26.080884 |        
       8 | A Brand New Task   | Test Description                 | 2022-05-08 21:03:25.409507 |        

 goal_id |                title                 
---------+--------------------------------------
       1 | Build a habit of going outside daily
       2 | Build a habit of sleeping at 11 pm
       3 | Build a habit of getting up at 7 am
"""

"""test_get_tasks_for_specific_goal """
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_one_goal(goal_id):
    goal = goal_id_validation(goal_id)
    goals = Goal.query.get(goal_id)
    #tasks = Task.query.all() #but where is this task_id from
    
    rsp = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks" : []
        #"tasks": json.dumps(tasks)
    }
    task_status = False
    print(len(goals.tasks))
    for task in goals.tasks:
        if task.completed_at is not None:
            task_status = True
        goals.tasks.append({
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task_status
    })
    print(len(goals.tasks))
    return make_response(jsonify(rsp), 200)
    
# @task_bp.route("/tasks/<goal_id>", methods=["GET"])
# def get_one_task_with_goal_id(goal_id):
#     goal = goal_id_validation(goal_id)
#     goal = Goal.query.get(goal_id)
    
#     task_status = False
#     for task in goal.tasks:
#         if "completed_at" in goal.tasks:
#             task_status = True
        
#         if task.goal_id == goal_id:
#             rsp = {
#                 "task": {
#                 "id": task.task_id,
#                 "goal_id": goal.goal_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": task_status
#             }}
        
#     return jsonify(rsp), 200