from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import requests
import os

SLACK_PATH = "https://slack.com/api/chat.postMessage"
SLACK_KEY = os.environ.get("SLACK_API_KEY")

tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"details": f"{task_id} is not valid input."}
        abort(make_response(jsonify(response), 400))
    
    task = Task.query.get(task_id)

    if not task:
        response = {"details": f"Task {task_id} does not exist."}
        abort(make_response(jsonify(response), 404))
    
    return task

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args
    if "sort" in params:
        if params["sort"] == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif params["sort"] == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    
    response = []
    for task in tasks:
        response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })

    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }

    return jsonify(response), 200


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                description=request_body["description"])
    except:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response), 400))
    
    if request_body.get("completed_at"):
        try:
            completed_at = str(request_body["completed_at"])
            finished = datetime.strptime(completed_at, 
                '%Y-%m-%d %H:%M:%S.%f')
            new_task.completed_at = finished
        except: # second to last test in wave 3 ends up here
            response = {"details": "Invalid date data"}
            abort(make_response(jsonify(response), 404))


    # try:
    #     if request_body.get("completed_at"):
    #         new_task = Task(title=request_body["title"],
    #             description=request_body["description"],
    #             completed_at=request_body["completed_at"])
    #             # When testing in Postman, make sure to add in format:
    #             # "2022-05-06"
    #     else:
    #         new_task = Task(title=request_body["title"],
    #             description=request_body["description"])
    # except:
    #     response = {"details": "Invalid data"}
    #     abort(make_response(jsonify(response), 400))

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }
    }

    return jsonify(response), 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    # Add check here to make sure both are provided
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }

    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }
    return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_mark_complete(task_id):
    task = validate_task(task_id)

    if not task.completed_at:
        task.completed_at = datetime.utcnow()
        db.session.commit()
        headers = {
            "Authorization": f"Bearer {SLACK_KEY}"
        }
        query_params = {
            "format": "json",
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}"
        }
        requests.get(SLACK_PATH, headers=headers, params=query_params)

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
        }
    }

    return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

    return jsonify(response), 200

#-------------------GOOOOOOOAAAAAALLLLSSS--------------------
goals_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response = {"details": f"{goal_id} is not valid input."}
        abort(make_response(jsonify(response), 400))
    
    goal = Goal.query.get(goal_id)

    if not goal:
        response = {"details": f"Goal {goal_id} does not exist."}
        abort(make_response(jsonify(response), 404))
    
    return goal

@goals_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response), 400))
    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }
    return jsonify(response), 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    
    response = []
    for goal in goals:
        response.append({
            "id": goal.goal_id,
            "title": goal.title
        })
    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    response = {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }
    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    
    # Add catch if title is not there or invalid input
    goal.title = request_body["title"]
    db.session.commit()

    response = {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }
    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_route(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}
    return jsonify(response), 200