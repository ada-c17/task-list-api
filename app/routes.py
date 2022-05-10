# import the necessary modules
from datetime import datetime
from app import db
from app.models.task import Task
from app.models.goal import Goal
# import dependencies
from flask import Blueprint, jsonify, make_response, request, abort
import os
import requests

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

# initialize Blueprint instance
# tasks blueprint
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
# goal blueprint
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task ID {task_id} is invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task ID {task_id} not found"}, 404))

    return task

@tasks_bp.route("", methods = ["POST"])
def add_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = datetime.utcnow())
    else: 
        new_task = Task(title = request_body["title"],
                    description = request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    rsp = {
        "id":new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        }

    if "completed_at" in request_body:
        rsp["is_complete"] = True
    else:
        rsp["is_complete"] = False
    
    return make_response({"task":rsp}, 201)


@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id":task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return make_response({"task":{"id":task.id,
                                "title": task.title,
                                "description": task.description,
                                "is_complete": False
                                }}, 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    if "completed_at" in request_body:
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = datetime.utcnow()
    else:
        task.title = request_body["title"]
        task.description = request_body["description"]

    db.session.commit()
    
    rsp = {
        "id":task.id,
        "title": task.title,
        "description": task.description}

    if "completed_at" in request_body:
        rsp["is_complete"] = True
    else:
        rsp["is_complete"] = False

    return make_response({"task":rsp}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f"Task {task.id} \"{task.title}\" successfully deleted"})


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()

    # call the Slack API and send out Slack messages
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
        }
    requests.post(slack_url, headers=headers, data=params)

    # get the response when marking complete on a completed task
    return make_response({"task":{"id":task.id,
                                "title": task.title,
                                "description": task.description,
                                "is_complete": True
                                }}, 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    return make_response({"task":{"id":task.id,
                                "title": task.title,
                                "description": task.description,
                                "is_complete": False
                                }}, 200)

#################### routes for Goal model #################### 
# helper function to validate goal 

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"Goal ID {goal_id} is invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"Goal ID {goal_id} not found"}, 404))

    return goal

@goals_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
        
    new_goal = Goal(title = request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()

    rsp = {
        "id":new_goal.goal_id,
        "title": new_goal.title
        }

    return make_response({"goal":rsp}, 201)

@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()
    tasks_response = []
    for goal in goals:
        tasks_response.append(
            {
                "id":goal.goal_id,
                "title": goal.title,
            }
        )
    return jsonify(tasks_response)

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return make_response({"goal":{"id":goal.goal_id,
                                "title": goal.title
                                }}, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    
    rsp = {
        "id":goal.goal_id,
        "title": goal.title}

    return make_response({"goal":rsp}, 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})



