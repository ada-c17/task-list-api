from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

PATH = "https://slack.com/api/chat.postMessage"
API_KEY = os.environ.get("SLACK_TOKEN")

goals_bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")

def validate_input(item_id, model_name):
    try:
        item_id = int(item_id)
    except ValueError:
        response = {"msg": f"Invalid id: {item_id}"}
        abort(make_response(jsonify(response), 400))

    chosen_item = model_name.query.get(item_id)    

    if chosen_item is None:
        response = {"msg": f"Could not find item with id {item_id}"}
        abort(make_response(jsonify(response), 404))
    return chosen_item

def task_body(task):
    return {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }

def create_task_dictionary(chosen_task):
    task_dict= {}
    task_dict["task"] = task_body(chosen_task)
    if chosen_task.goal_id:
            task_dict["task"].update({"goal_id": chosen_task.goal_id})

    return task_dict

def create_goal_dictionary(chosen_goal):
    goal_dict= {}
    goal_dict["goal"] = {
            "id": chosen_goal.goal_id,
            "title": chosen_goal.title,
        }
    return goal_dict

def create_slack_api_request(chosen_task):
    params = {
        "text": f"Someone just completed the task {chosen_task.title}",
        "channel": "task-notifications"
        }
    hdrs = {
        "Authorization": f"Bearer {API_KEY}"
    }
    r = requests.post(PATH, data = params, headers = hdrs)
    return r

@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goal_response = []
    for goal in goals:
        goal_response.append({
            "id": goal.goal_id,
            "title": goal.title,
            })
    return jsonify(goal_response), 200

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    chosen_goal = validate_input(goal_id, Goal)
    response = create_goal_dictionary(chosen_goal)
    return jsonify(response), 200

@goals_bp.route("", methods = ["POST"])
def create_one_goal():
    request_body = request.get_json()
    try:
        chosen_goal = Goal(title = request_body["title"])
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(chosen_goal)
    db.session.commit()
    response = create_goal_dictionary(chosen_goal)
    return jsonify(response), 201

@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_goal_complete(goal_id):
    chosen_goal = validate_input(goal_id, Goal)
    request_body = request.get_json()
    try:
        chosen_goal.title = request_body["title"]
    except KeyError:
        return {
            "msg": "title is required"
        }, 400
    db.session.commit()
    response = create_goal_dictionary(chosen_goal)
    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_one_goal(goal_id):
    chosen_goal = validate_input(goal_id, Goal)
    db.session.delete(chosen_goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'
    }, 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def place_tasks_on_goal(goal_id):
    goal = validate_input(goal_id, Goal)
    request_body = request.get_json()

    found_tasks = [validate_input(task, Task) for task in request_body["task_ids"] if validate_input(task, Task)]

    goal.tasks = found_tasks
    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
        }, 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_input(goal_id, Goal)
    task_response = []
    for task in goal.tasks:
        task_dict = task_body(task)
        task_dict["goal_id"] = goal.goal_id
        task_response.append(task_dict)
        
    return jsonify({"id": goal.goal_id,
                    "title": goal.title,
                    "tasks": task_response
    }), 200
    
