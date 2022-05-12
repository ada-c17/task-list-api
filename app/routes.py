from datetime import datetime
from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
import os
import requests
token=os.environ.get("SLACK_BOT_TOKEN")

# Blueprints
task_bp = Blueprint("Tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("Goals", __name__, url_prefix="/goals")

# Helper Functions
def error_message(message, status_code):
    abort(make_response({"details":message}, status_code))

def post_to_slack(channel, message):
    url = "https://slack.com/api/chat.postMessage"
    params = {
        "channel":channel,
        "text":message,
        "pretty":1
    }
    headers = {"Authorization": f"Bearer {token}"}
    requests.post(url, params=params, headers=headers)

# Task Routes
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        error_message("Invalid data", 400)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

@task_bp.route("", methods=["GET"])
def get_tasks():
    if request.args.get("sort") or request.args.get("sort_by"):
        tasks = Task.sort()
    else:
        tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

@task_bp.route("/<id>", methods=["GET"])
def get_task(id):
    task = Task.validate(id)
    return {"task": task.to_dict()}

@task_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = Task.validate(id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))

@task_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = Task.validate(id)

    task.completed_at = datetime.utcnow()
    db.session.commit()
    message = f"Someone just completed the task {task.title}"
    channel = "task-notifications"
    post_to_slack(channel, message)

    return make_response(jsonify({"task": task.to_dict()}))

@task_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = Task.validate(id)

    task.completed_at = None
    
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))

@task_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = Task.validate(id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({
        "details": 
            f"Task {task.id} \"{task.title}\" successfully deleted"}))

# Goal Routes
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        error_message("Invalid data", 400)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

@goal_bp.route("", methods=["GET"])
def get_goals():
    if request.args.get("sort") or request.args.get("sort_by"):
        goals = Goal.sort()
    else:
        goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)

@goal_bp.route("/<id>", methods=["GET"])
def get_goal(id):
    goal = Goal.validate(id)
    return {"goal": goal.to_dict()}

@goal_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = Goal.validate(id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}))

@goal_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = Goal.validate(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({
        "details": 
            f"Goal {goal.id} \"{goal.title}\" successfully deleted"
            }))

#One-to-Many Routes
@goal_bp.route("<id>/tasks", methods=["POST"])
def post_task_ids_to_goal(id):
    goal = Goal.validate(id)
    task_ids = request.get_json()["task_ids"]
    for id in task_ids:
        Task.query.get(id).goal_id = goal.id

    db.session.commit()

    return make_response(jsonify({"id": goal.id, "task_ids": task_ids}))

@goal_bp.route("<id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(id):
    goal = Goal.validate(id)
    return goal.to_dict_with_tasks()
