from flask import Blueprint, request,jsonify, make_response, abort
from app.models.task import Task
from app.models.goal import Goal 
from app import db 
from sqlalchemy import desc, asc
from datetime import datetime 
import requests
import os  
from pprint import pprint 

PATH = "https://slack.com/api/chat.postMessage?channel=task-notifications&text="

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
    else:
        new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete(new_task)
        }
    }, 201


def is_complete(task):
    if not task.completed_at:
        return False 
    else:
        return True 


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        # response = {"message": f"Could not retrieve task with id {task_id}"} 
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

        # return abort(make_response(jsonify(response), 404))
    
    task = Task.query.get(task_id)
    if not task:
            abort(make_response({"message":f"Task {task_id} not found"}, 404))

    # if task is None:
    #     response = {"message": f"Invalid ID: {task_id}"}
    #     return response, 400 
    
    return task 


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()
    
    headers = { "Authorization": "Bearer " + os.environ.get(
            "SLACK_API_TOKEN") }
    
    requests.post(PATH + f"Someone just completed the task {task.title}", headers=headers)

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete(task)
        }
    }, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete(task)
        }
    }, 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_task(task_id)

    if task.goal_id:
        return make_response(jsonify({
            "task": {
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_complete(task)
            }
        })), 200
    else:
        return make_response(jsonify({
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_complete(task)
            }
    })), 200


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args 
    if "sort" in params:
        sort = params["sort"]
        if sort.lower() == "asc":
            tasks = Task.query.order_by(asc(Task.title)).all()
        elif sort.lower() == "desc":
            tasks = Task.query.order_by(desc(Task.title)).all()
    else:    
        tasks = Task.query.all()

    tasks_response = []

    if len(tasks) == 0:
        return jsonify(tasks_response), 200

    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete(task)
        })
    
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    print(task)
    # updated_task = None
    if "title" and "description" in request_body:
        # updated_task.title = request_body["title"]
        # updated_task.description = request_body["description"]
        task.title = request_body["title"]
        task.description = request_body["description"]
    else: 
        return {"details": "Invalid data"}, 400

    
    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete(task)
        }
    }, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }), 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return abort(make_response({"message":f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if goal is None:
        abort(make_response({"message":f"Goal {goal_id} not found"}, 404))

    return goal 


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
        })
    
    return jsonify(goals_response), 200
    
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = validate_goal(goal_id)

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title 
        }
    }, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    else:
        goal.title = request_body["title"]
    
    db.session.commit()

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }
    }, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }, 200


@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def create_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)
    tasks = []
    retrieved_tasks = []
    request_body = request.get_json()

    if "task_ids" in request_body:
        tasks = request_body["task_ids"]

    for task in tasks:
        task = validate_task(task)
        if task:
            retrieved_tasks.append(task)
    
    goal.tasks = retrieved_tasks
    db.session.commit()
        
    return {
        "id": goal.goal_id,
        "task_ids": tasks 
    }, 200


@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)
    tasks_response = []

    tasks = goal.tasks 
    for task in tasks:
        tasks_response.append({
            "id": task.task_id, 
            "goal_id": task.goal_id,
            "title": task.title, 
            "description": task.description, 
            "is_complete": is_complete(task)
        })
    
    return {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
    }, 200

