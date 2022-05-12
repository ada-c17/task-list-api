# import the necessary modules
from datetime import datetime
from app import db
from app.routes.task_routes import validate_task
from app.models.goal import Goal
# import dependencies
from flask import Blueprint, jsonify, make_response, request, abort
import os
import requests


# initialize Blueprint instance
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

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

    return make_response({"goal":new_goal.to_json()}, 201)

@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()

    tasks_response = []
    for goal in goals:
        tasks_response.append(goal.to_json())

    return jsonify(tasks_response)

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return make_response({"goal":goal.to_json()}, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    
    return make_response({"goal":goal.to_json()}, 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})

#################### connect tasks to goals #################### 
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_task(task_id)
        goal.tasks.append(task)

    db.session.commit()

    rsp = {
        "id":goal.goal_id,
        "task_ids": request_body["task_ids"]}

    return make_response(rsp)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_goal(goal_id):
    goal = validate_goal(goal_id)
    tasks_response = []

    for task in goal.tasks:
        tasks_response.append({
            "goal_id":goal.goal_id,
            "id":task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
            })

    rsp =  {
        "id":goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response}

    return make_response(rsp)



