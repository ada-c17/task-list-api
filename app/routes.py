from flask import Blueprint, jsonify, make_response, request, abort
from requests import session
from app.models.task import Task
from app.models.goal import Goal
from app.models.helper import validate_id, validate_data, validate_goal_id, validate_goal
from app import db
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os 

task_db = Blueprint("tasks",__name__, url_prefix = "/tasks")
goal_db = Blueprint("goals", __name__, url_prefix = "/goals")


@task_db.route("", methods = ["GET"])
def get_all_tasks():
    task_response = []
    sort_query = request.args.get("sort")
    if not sort_query:
        ordered_tasks = Task.query.all()
    elif sort_query == "asc":
        ordered_tasks = Task.query.order_by(asc(Task.title)).all()
    elif sort_query == "desc":
        ordered_tasks = Task.query.order_by(desc(Task.title)).all()
    
    for task in ordered_tasks:
        task_response.append(task.to_json())
    return jsonify(task_response), 200

@task_db.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task_response = []
    task = validate_id(task_id)
    return jsonify({"task": task.to_json()}), 200

@task_db.route("", methods = ["POST"])
def create_one_response():
    request_body = request.get_json()
    valid_data = validate_data(request_body)
    new_task = Task.create_task(valid_data)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task":new_task.to_json()}), 201
    

@task_db.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = validate_id(task_id)
    request_body = request.get_json()
    task.update_task(request_body)
    
    db.session.commit()
    return jsonify({"task":task.to_json()}), 200

@task_db.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = validate_id(task_id)
    task_title = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return {
        "details": f'Task {task_id} \"{task_title.title}\" successfully deleted'}, 200 

@task_db.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_task_complete(task_id):
    task = validate_id(task_id)
    
    task.completed_at = datetime.now()

    db.session.commit()
    return jsonify({"task":task.to_json()}), 200

@task_db.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_id(task_id)

    task.completed_at = None

    db.session.commit()
    return jsonify({"task":task.to_json()}), 200

# TOKEN = os.environ["SLACK_TOKEN"]
# SLACK_URL = os.environ["SLACK_URL"]
# @task_db.route("/<task_id>/mark_complete", methods = ["PATCH"])
# def mark_task_complete_by_slack_bot(task_id):
#     task = validate_id(task_id)
#     validated_task = task.query.get(task_id)
#     task.completed_at = datetime.now()

#     authorize = {"Authorization":f"Bearer {TOKEN}"}
#     data = {
#         "channel":"task-notifications",
#         "text": f"Someone just completed the {task.title}."
#     }
#     req = requests.post(SLACK_URL, authorize=authorize, data=data)

#     db.session.commit()
#     return jsonify({"task":task.to_json()}), 200


@goal_db.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    goal_response = []
    goal = validate_goal_id(goal_id)
    return jsonify({"goal": goal.goal_to_json()}), 200

@goal_db.route("", methods = ["GET"])
def get_all_goals():
    goal_response = []
    goals = Goal.query.all()
    for goal in goals:
        goal_response.append(goal.goal_to_json())

    return jsonify(goal_response), 200

@goal_db.route("", methods = ["POST"])
def create_one_goals():
    request_body = request.get_json()
    is_valid = validate_goal(request_body)
    new_goal = Goal.create_goal(is_valid)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.goal_to_json()}), 201

@goal_db.route("/<goal_id>", methods = ["DELETE"])
def delete_task(goal_id):
    goal = validate_goal_id(goal_id)
    goal_title = Goal.query.get(goal_id)
    db.session.delete(goal_title)
    db.session.commit()
    return {
        "details": f'Goal {goal_id} \"{goal_title.title}\" successfully deleted'}, 200 

@goal_db.route("/<goal_id>", methods = ["PUT"])
def update_task(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    goal.update_goal(request_body)
    
    db.session.commit()
    return jsonify({"Goal":goal.goal_to_json()}), 200
