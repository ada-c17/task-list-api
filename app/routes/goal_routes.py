import requests
import os
from flask import Blueprint, jsonify, request
from app.models.goal import Goal
from app.models.task import Task
from app import db
from app.routes.helper_functions import get_record_by_id, error_message

# Routes for Goal

bp = Blueprint("goals_bp",__name__, url_prefix="/goals")

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
    goal = get_record_by_id(goal_id, Goal)
    goal_dict = goal.make_dict()

    request_body = request.get_json()

    tasks = [get_record_by_id(task_id, Task) for task_id in request_body["task_ids"]]

    goal.tasks = tasks

    # for task_id in request_body["task_ids"]:
    #     task = get_record_by_id(task_id, Task)
    #     task.goal_id = goal_id

    db.session.commit()

    return jsonify({"id": goal_dict["id"], "task_ids": request_body["task_ids"]})

# GET /goals
@bp.route("", methods=["GET"])
def list_goals():

    goals = Goal.query.all()
    goal_list = [goal.make_dict() for goal in goals]

    return jsonify(goal_list)

# GET /goals/<goal_id>
@bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = get_record_by_id(goal_id, Goal)

    return jsonify({"goal": goal.make_dict()})

# GET /goals/<goal_id>/tasks
@bp.route("/<goal_id>/tasks", methods=["GET"]) 
def get_tasks_of_one_goal(goal_id):
    goal = get_record_by_id(goal_id, Goal)
    goal_dict = goal.make_dict()

    task_list = [task.make_dict() for task in goal.tasks]

    return jsonify({"id": goal_dict["id"], "title": goal_dict["title"], "tasks": task_list})

# PUT /goals/<goal_id>
@bp.route("/<goal_id>", methods=["PUT"])
def replace_task_by_id(goal_id):
    request_body = request.get_json()
    goal = get_record_by_id(goal_id, Goal)

    try: 
        goal.replace_title(request_body)
    except KeyError as error:
        error_message(f"Missing key: {error}", 400)

    db.session.commit()

    return jsonify({"goal": goal.make_dict()})

# DELETE /goals/<goal_id>
@bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal_by_id(goal_id):
    goal = get_record_by_id(goal_id, Goal)

    db.session.delete(goal)
    db.session.commit()

    goal_dict = goal.make_dict()
    return jsonify({'details': f'Goal {goal_id} "{goal_dict["title"]}" successfully deleted'})