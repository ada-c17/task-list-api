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

def validate(type, id):
    try:
        id = int(id)
    except:
        error_message(f"{type} {id} invalid", 400)
    if type == "task":
        valid = Task.query.get(id)
    if type == "goal":
        valid = Goal.query.get(id)
    if not valid:
        error_message(f"{type} {id} not found", 404)

    return valid

# Task Routes
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError as err:
        error_message("Invalid data", 400)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

@task_bp.route("", methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

@task_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate("task", task_id)
    return {"task": task.to_dict()}

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate("task", task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate("task", task_id)
    task.completed_at = datetime.utcnow()
    
    db.session.commit()
    url = "https://slack.com/api/chat.postMessage"
    message = f"Someone just completed the task {task.title}"
    params = {
        "channel":"task-notifications",
        "text":message,
        "pretty":1
    }
    headers = {"Authorization": f"Bearer {token}"}
    requests.post(url, params=params, headers=headers)

    # try:
    #     result = client.chat_postMessage(
    #     channel="C03EJMV4R44", 
    #     text=f"Someone just completed the task {task.title}"
    #     )
    #     logger.info(result)

    # except SlackApiError as e:
    #     logger.error(f"Error posting message: {e}")


    return make_response(jsonify({"task": task.to_dict()}))

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate("task", task_id)
    task.completed_at = None
    
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate("task", task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}))

# Goal Routes
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError as err:
        error_message("Invalid data", 400)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

@goal_bp.route("", methods=["GET"])
def get_goals():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(Goal.title).all()
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = validate("goal", goal_id)
    return {"goal": goal.to_dict()}

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate("goal", goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}))

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate("goal", goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}))

#One-to-Many Routes
@goal_bp.route("<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate("goal", goal_id)
    task_ids = request.get_json()["task_ids"]
    for id in task_ids:
        Task.query.get(id).goal_id = goal.goal_id

    db.session.commit()

    return make_response(jsonify({"id": goal.goal_id, "task_ids": task_ids}))

@goal_bp.route("<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
    goal = validate("goal", goal_id)
    return jsonify(goal.to_dict_with_tasks())
