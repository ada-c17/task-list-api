from flask import Blueprint, request,jsonify, make_response, abort
from app.models.goal import Goal 
from app.models.task import Task 
from app import db 
from sqlalchemy import desc, asc
from datetime import datetime 
import requests
import os  

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def is_complete(task):
    if not task.completed_at:
        return False 
    else:
        return True 

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))
    
    return task 


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

