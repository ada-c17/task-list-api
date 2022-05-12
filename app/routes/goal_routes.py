import requests
import os
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db
from app.routes.task_routes import get_task_record_by_id

# Routes for Goal

bp = Blueprint("goals_bp",__name__, url_prefix="/goals")

# helper functions
def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def get_goal_record_by_id(id):
    try: 
        id = int(id)
    except ValueError:
        error_message(f"Invalid goal id {id}", 400)
    
    goal = Goal.query.get(id)

    if goal:
        return goal
    
    error_message(f"No goal with id {id} found", 404)

# POST /goals
@bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        goal = Goal.from_dict(request_body)
    except KeyError:
        error_message(f"Invalid data", 400)

    db.session.add(goal)
    db.session.commit()

    return jsonify({"goal": goal.make_dict()}), 201

# POST /goals/<goal_id>/tasks
@bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = get_goal_record_by_id(goal_id)
    goal_dict = goal.make_dict()

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = get_task_record_by_id(task_id)
        task.goal_id = goal_id

    db.session.commit()

    return jsonify({"id": goal_dict["id"], "task_ids": request_body["task_ids"]})

# GET /goals
@bp.route("", methods=["GET"])
def list_goals():

    goals = Goal.query.all()
    list_of_goals = [goal.make_dict() for goal in goals]

    return jsonify(list_of_goals)

# GET /goals/<goal_id>
@bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)

    return jsonify({"goal": goal.make_dict()})

# GET /goals/<goal_id>/tasks
@bp.route("/<goal_id>/tasks", methods=["GET"]) 
def get_tasks_of_one_goal(goal_id):
    goal = get_goal_record_by_id(goal_id)
    goal_dict = goal.make_dict()

    task_list = []
    for task in goal.tasks:
        task_list.append(task.make_dict())

    return jsonify({"id": goal_dict["id"], "title": goal_dict["title"], "tasks": task_list})

# PUT /goals/<goal_id>
@bp.route("/<goal_id>", methods=["PUT"])
def replace_task_by_id(goal_id):
    request_body = request.get_json()
    goal = get_goal_record_by_id(goal_id)

    try: 
        goal.replace_title(request_body)
    except KeyError as error:
        error_message(f"Missing key: {error}", 400)

    db.session.commit()

    return jsonify({"goal": goal.make_dict()})

# DELETE /goals/<goal_id>
@bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    goal = goal.make_dict()
    return jsonify({'details': f'Goal {goal_id} "{goal["title"]}" successfully deleted'})