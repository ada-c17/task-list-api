from urllib import response
from app.models.task import Task
from app import db
from app.models.goal import Goal
import os
import datetime

# from ..helpers import validate_goal
from ..helpers import validate_object
# from ..helpers import validate_task
from flask import Blueprint, request, jsonify, make_response, abort

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_json()["goal"] for goal in goals]
    return jsonify(goals_response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def handle_goal(goal_id):
    goal = validate_object(Goal, goal_id)
    return jsonify(goal.to_json()), 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def handle_goal_task(goal_id):
    goal = validate_object(Goal, goal_id)
    response = goal.to_json_task()
    for item in goal.tasks:  # for every task in goals
        response["tasks"].append(item.to_json()["task"])
    return jsonify(response), 200


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.create(request_body)
        db.session.add(new_goal)
        db.session.commit()

    except KeyError:
        return abort(make_response(jsonify({"details": "Invalid data"}), 400))

    return new_goal.to_json(), 201

# refactor


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task_list(goal_id):
    goal = validate_object(Goal, goal_id)  # goal query
    request_body = request.get_json()
    task_list = []
    for item in request_body["task_ids"]:
        task_list.append(item)
        goals_task = Task.query.get(item)
        goal.tasks.append(goals_task)

    db.session.commit()
    return ({"id": int(goal_id), "task_ids": task_list}, 200)


@ goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_object(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()
    return goal.to_json(), 200


@ goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_object(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200
