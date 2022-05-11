
# from requests import request
import requests
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from .helper import validate_task, validate_goal
from sqlalchemy import asc, desc
from datetime import datetime
from dotenv import load_dotenv
import os


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
load_dotenv()

# CREATE task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        if 'completed_at' in request_body:
            new_task = Task.create_complete(request_body)
        else:
            new_task = Task.create_incomplete(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.add(new_task)
    db.session.commit()

    response_body = {}
    response_body['task'] = new_task.to_json()

    return make_response(jsonify(response_body), 201)


# GET ALL tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == 'asc':
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == 'desc':
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200

# GET one task
@tasks_bp.route("/<task_id>", methods=["GET"])  
def read_one_task(task_id):
    task = validate_task(task_id)

    return make_response({"task": task.to_json()}, 200)

# UPDATE one task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    try:
        if 'completed_at' in request_body:
            task.title = request_body["title"]
            task.description = request_body["description"]
            task.completed_at = request_body["completed_at"]
        else:
            task.title = request_body["title"]
            task.description = request_body["description"]
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.commit()

    response_body = {}
    response_body['task'] = task.to_json()
    # response_body['task'] = {
    #     "id": task.task_id,
    #     "title": task.title,
    #     "description": task.description,
    #     "is_complete": True if task.completed_at else False
    # }

    return make_response(jsonify(response_body), 200)
    

# DELETE one task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details":f'Task {task.task_id} "{task.title}" successfully deleted'})), 200
    

# Mark task as complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_completed(task_id):
    task = validate_task(task_id)

    path = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("SLACK_API")
    head = {"Authorization":API_KEY}

    query_params = {
        "channel": "task-notifications",
        "text": "Someone just completed the task My Beautiful Task"
    }

    task.completed_at = datetime.today()
    req = requests.post(path, headers=head,params=query_params)

    db.session.commit()

    response_body = {}
    response_body['task'] = task.to_json()

    return make_response(jsonify(response_body), 200)

# Mark task as incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None

    db.session.commit()

    response_body = {}
    response_body['task'] = task.to_json()

    return make_response(jsonify(response_body), 200)

# ------------------------- Goal part -------------------------

# # CREATE goal
# @goals_bp.route("", methods=["POST"])
# def create_goal():
#     request_body = request.get_json()

#     try:
#         new_goal = Goal(
#             title=request_body['title']
#     )
#     except KeyError:
#         return abort(make_response(jsonify({"details":"Invalid data"}), 400))
    
#     # new_goal = Goal(
#     #     title=request_body['title']
#     # )
        
#     db.session.add(new_goal)
#     db.session.commit()

#     response_body = {}
#     response_body['goal'] = {
#         "id": new_goal.goal_id,
#         "title": new_goal.title
#     }

#     return make_response(jsonify(response_body), 201)


# # GET ALL goals
# @goals_bp.route("", methods=["GET"])
# def read_all_goals():
#     goals = Goal.query.all()

#     goals_response = []
#     for goal in goals:
#         goals_response.append(goal.to_json())

#     return jsonify(goals_response), 200

# # GET one goal
# @goals_bp.route("/<goal_id>", methods=["GET"])  
# def read_one_goal(goal_id):
#     goal = validate_goal(goal_id)
#     return jsonify({
#         "goal": goal.to_json()
#         })


# # UPDATE one goal
# @goals_bp.route("/<goal_id>", methods=["PUT"])
# def update_goal(goal_id):
#     goal = validate_goal(goal_id)
#     request_body = request.get_json()

#     try:
#         goal.title = request_body["title"]
#     except KeyError:
#         return abort(make_response(jsonify({"details":"Invalid data"}), 400))

#     db.session.commit()

#     response_body = {}
#     response_body['goal'] = {
#         "id": goal.goal_id,
#         "title": goal.title
#     }

#     return make_response(jsonify(response_body), 200)

# # DELETE one goal
# @goals_bp.route("/<goal_id>", methods=["DELETE"])
# def delete_goal(goal_id):
#     goal = validate_goal(goal_id)

#     db.session.delete(goal)
#     db.session.commit()

#     return make_response(jsonify({"details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})), 200

# --------------------------Wave_6 one to many ------------------------------

# @goals_bp.route("/<goal_id>/tasks", methods=["POST"])  # do we need /goals/<goal_id>/tasks or /<goal_id>/tasks
# def create_list_tasks_to_goal(goal_id):

#     goal = validate_goal(goal_id)

#     request_body = request.get_json()

#     new_task1 = Task(
#         title=request_body["title"],
#         description=request_body["description"],
#         goal = goal
#     )

#     new_task2 = Task(
#         title=request_body["title"],
#         description=request_body["description"],
#         goal = goal
#     )

#     new_task3 = Task(
#         title=request_body["title"],
#         description=request_body["description"],
#         goal = goal
#     )
#     db.session.add(new_task1.task_id, new_task2.task_id, new_task3.task_id)
#     db.session.commit()
#     return make_response(jsonify({"id": {goal_id}, "task_ids": [1, 2, 3]}), 201)


# @goals_bp.route("/<goal_id>/tasks", methods=["GET"])
# def read_tasks_of_one_goal(goal_id):

#     goal = validate_goal(goal_id)
#     tasks_response = []

#     if goal.tasks == []:
#             response_body = {
#                 "id": goal.goal_id,
#                 "title": goal.title,
#                 "tasks": tasks_response
#             }
#             return make_response(jsonify(response_body), 200)
    
#     for task in goal.tasks:
#         tasks_response.append(
#             {
#                 "id": task.task_id,
#                 "goal_id": goal.goal_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": True if task.completed_at else False
#             }
#         )

#     response_body = {
#         "id": goal.goal_id,
#         "title": goal.title,
#         "tasks": tasks_response
#     }

#     return make_response(jsonify(response_body), 200)

# @goals_bp.route("/<task_id>", methods=["GET"])
# def get_task_includes_goal_id(task_id):
#     task = validate_task(task_id)

#     response_body = {}
#     response_body["task"] = {
        
#         "id": task.task_id,
#         "goal_id": task.goal_id,
#         "title": task.title,
#         "description": task.description,
#         "is_complete": True if task.completed_at else False

#     }
    
#     return  make_response(jsonify(response_body), 200)

    



    
