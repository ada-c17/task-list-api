
from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.task import tasks_bp

from datetime import datetime
import os
import requests

goals_bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    goal = Goal(
        title = request_body["title"]
    )

    db.session.add(goal)
    db.session.commit()

    response = {
        "id": goal.goal_id,
        "title": goal.title
        }
    
    return jsonify({"goal": response}), 201


@goals_bp.route("", methods=["GET"])
def get_goals():
    response = []
    sort_by = request.args.get('sort')
    if sort_by == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    elif sort_by == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()

    for goal in goals:
        response.append({
            'id': goal.goal_id,
            'title': goal.title,
        })
    return jsonify(response)


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"Goal id '{goal_id}' is invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"Goal id '{goal_id}' not found"}, 404))

    return goal


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    response = {
        "id": goal.goal_id,
        "title": goal.title
        }

    return jsonify({"goal": response}), 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response = {
        "id": goal.goal_id,
        "title": goal.title,
        }

    return make_response({"goal": response})

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = {
    "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
    }

    return jsonify(response), 200

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task id '{task_id}' is invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task id '{task_id}' not found"}, 404))

    return task

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goals(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    task_ids = request_body["task_ids"]
    for task in task_ids:
        chosen_task = validate_task(task)
        chosen_task.goal_id = goal.goal_id
    
    db.session.commit()

    return {
    "id": goal.goal_id,
    "task_ids": task_ids
}