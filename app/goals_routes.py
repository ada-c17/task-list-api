import os
from os import abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime, timezone
import requests 
from dotenv import load_dotenv

load_dotenv()

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    response_body = []
    goals = Goal.query.all()

    for goal in goals: 
        response = goal.make_goal_dict()
        response_body.append(response)
    return jsonify(response_body), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    goal_dict = {"goal": goal.make_goal_dict()}
    return jsonify(goal_dict), 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    goal_dict = {"goal": new_goal.make_goal_dict()}

    return jsonify(goal_dict), 201

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    goal_dict = {"goal": goal.make_goal_dict()}

    return jsonify(goal_dict), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    request_body = request.get_json()
    
    if "task_ids" not in request_body:
        abort(make_response({"Message": "Please give a list of task ids."}, 400))

    task_id_list = []
    for task_id in request_body["task_ids"]:
        task = Task.validate_task(task_id)
        task.goal_id = goal.goal_id
        task_id_list.append(task.id)

    db.session.commit()
    
    return jsonify({"id": goal.goal_id, "task_ids": task_id_list}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    goal_dict = Goal.make_goal_dict(goal)
    goal_dict["tasks"] = []
    
    tasks = Goal.query.get(goal.goal_id).tasks
    for task in tasks:
        task_dict = task.make_task_dict()
        goal_dict["tasks"].append(task_dict)
    
    return jsonify(goal_dict), 200
