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


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")
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

def create_task_dictionary(chosen_task):
    task_dict= {}
    if chosen_task.completed_at is None:
        if chosen_task.goal_id:
            task_dict["task"] = {
                "id": chosen_task.task_id,
                "goal_id": chosen_task.goal_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": False
            }
        else:
            task_dict["task"] = {
            "id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": False
        }
    else:
        if chosen_task.goal_id:
            task_dict["task"] = {
                "id": chosen_task.task_id,
                "goal_id":chosen_task.goal_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": True
            }
        else:
            task_dict["task"] = {
                "id": chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": True
            }
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




@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    params = request.args
    if params and params["sort"] == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif params and params["sort"] == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()
    task_response = []
    for task in tasks:
        if task.completed_at is None:
            task_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            })
        else: 
            task_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": True
            })
    return jsonify(task_response), 200

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    chosen_task = validate_input(task_id, Task)
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200

@tasks_bp.route("", methods = ["POST"])
def create_one_task():
    request_body = request.get_json()
    try:
        if request_body.get("completed_at"):
            chosen_task = Task( title = request_body["title"],
                        description = request_body["description"],
                        completed_at = request_body["completed_at"]
                        )
        else:
            chosen_task = Task( title = request_body["title"],
                        description = request_body["description"]
                        )
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(chosen_task)
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 201

@tasks_bp.route("/<task_id>", methods = ["PUT"])
def add_one_task(task_id):
    chosen_task = validate_input(task_id, Task)
    request_body = request.get_json()
    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
    except KeyError:
        return {
            "msg": "title and description are required"
        }, 400
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    chosen_task = validate_input(task_id, Task)
    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{chosen_task.title}" successfully deleted'
    }, 200

@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def update_task_complete(task_id):
    chosen_task = validate_input(task_id, Task)
    chosen_task.completed_at = datetime.utcnow()
    create_slack_api_request(chosen_task)
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def update_task_incomplete(task_id):
    chosen_task = validate_input(task_id, Task)
    chosen_task.completed_at = None
    db.session.commit()
    response = create_task_dictionary(chosen_task)
    return jsonify(response), 200


#****** routes for goals ******

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
    found_tasks= []

    for task in request_body["task_ids"]:
        found_task = validate_input(task, Task)
        if found_task:
            found_tasks.append(found_task)
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
        if task.completed_at is None:
            if task.goal_id:
                task_response.append(
                    {
                        "id": task.task_id,
                        "goal_id": goal.goal_id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": False
                    }
                )
        else:
            task_response.append(
                {
                    "id": task.task_id,
                    "goal_id": goal.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": True
                }
            )
    return jsonify({"id": goal.goal_id,
                    "title": goal.title,
                    "tasks": task_response
    }), 200
    
