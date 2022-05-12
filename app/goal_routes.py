import json, os, requests
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes_helper import validate_goal, validate_task

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        abort(make_response(jsonify(dict(details="Invalid data")), 400))
    
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify(dict(goal=new_goal.to_dict())), 201)

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goals_response))

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal_data = validate_goal(goal_id)

    return make_response(jsonify(dict(goal=goal_data.to_dict())))

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal_data = validate_goal(goal_id)
    request_body = request.get_json()

    goal_data.title = request_body["title"]

    db.session.commit()
    return make_response(jsonify(dict(goal=goal_data.to_dict())))

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal_data = validate_goal(goal_id)

    db.session.delete(goal_data)
    db.session.commit()
    return make_response(jsonify(dict(details=f'Goal {goal_data.goal_id} "{goal_data.title}" successfully deleted')))

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    request_body_ids = request_body["task_ids"]

    for task_id in request_body_ids:
        task = validate_task(task_id)
        task.goal = goal

    db.session.commit()
    return make_response(jsonify(dict(id=int(goal_id), task_ids=request_body_ids)))

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_goal(goal_id):
    goal = validate_goal(goal_id)
    
    tasks_in_goal = []
    for task in goal.tasks:
        task_dict = task.to_dict()
        task_dict["goal_id"] = int(goal_id)
        tasks_in_goal.append(task_dict)
    
    return make_response(jsonify(dict(
        id=int(goal_id),
        title=goal.title,
        tasks=tasks_in_goal
    )))