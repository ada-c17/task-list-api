from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
from dotenv import load_dotenv
import os, requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        new_task = Task(title=request_body["title"], 
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
    else:
        new_task = Task(title=request_body["title"], 
                description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": new_task.create_task_dict()
    }
    return response, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_sort_query = request.args.get("sort")
    if title_sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append(task.create_task_dict())

    return jsonify(response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_one_task_or_abort(task_id)
    response = {
        "task": task.create_task_dict()
    }
    return response

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"msg":f"Invalid task id: {task_id}. ID must be an integer."}
        abort(make_response(jsonify(response), 400))
    
    requested_task = Task.query.get(task_id)
    if requested_task is None:
        response = {"msg":f"Could not find task with id: {task_id}"}
        abort(make_response(jsonify(response), 404))
        
    return requested_task

@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    task = get_one_task_or_abort(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    response = {
        "task": task.create_task_dict()
    }
    return response

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_one_task_or_abort(task_id)
    db.session.delete(task)
    db.session.commit()
    response = {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}
    return response

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = get_one_task_or_abort(task_id)
    task.completed_at = datetime.now()

    db.session.commit()
    response = {
        "task": task.create_task_dict()
    }

    path = "https://slack.com/api/chat.postMessage"
    data = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    headers = {
        "authorization": "Bearer " + os.environ.get("SLACKBOT_API_KEY")
    }

    post_message = requests.post(path, data=data, headers=headers)

    return response

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = get_one_task_or_abort(task_id)
    task.completed_at = None
    db.session.commit()
    response = {
        "task": task.create_task_dict()
    }
    return response

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal": new_goal.create_goal_dict()
    }
    return response, 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response = []
    for goal in goals:
        response.append(
            goal.create_goal_dict()
        )

    return jsonify(response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = get_one_goal_or_abort(goal_id)
    response = {
        "goal": goal.create_goal_dict()
    }
    return response

def get_one_goal_or_abort(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response = {"msg":f"Invalid goal id: {goal_id}. ID must be an integer."}
        abort(make_response(jsonify(response), 400))
    
    requested_goal = Goal.query.get(goal_id)
    if not requested_goal:
        response = {"msg":f"Could not find goal with id: {goal_id}"}
        abort(make_response(jsonify(response), 404))
        
    return requested_goal

@goals_bp.route("/<goal_id>", methods=["PUT"])
def replace_goal(goal_id):
    goal = get_one_goal_or_abort(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()
    response = {
        "goal": goal.create_goal_dict()
    }
    return response

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_one_goal_or_abort(goal_id)

    db.session.delete(goal)
    db.session.commit()
    response = {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}

    return response

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def associate_tasks_goals(goal_id):
    goal = get_one_goal_or_abort(goal_id)
    request_body = request.get_json()

    try:
        task_ids = request_body["task_ids"]
    except KeyError:
        return {"msg": "Missing task_ids in request body"}, 400
    
    if not isinstance(task_ids, list):
        return {"msg": "Expected list of task ids"}, 400
    
    tasks = []
    for id in task_ids:
        tasks.append(get_one_task_or_abort(id))
        
    for task in tasks:
        task.goal = goal
    
    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": task_ids
    }, 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_assoc_goal(goal_id):
    goal = get_one_goal_or_abort(goal_id)
    request_body = request.get_json()

    goal_tasks = []
    for task in goal.tasks:
        goal_tasks.append(task)
    
    response = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []
    }
    
    for task in goal.tasks:
        response["tasks"].append(task.create_task_dict())

    return response
