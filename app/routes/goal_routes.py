from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, make_response, request, jsonify, abort
from .helpers import validate_goal, validate_task
import requests
import os


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# Get goals
@goals_bp.route("", methods=["GET"])
def get_goals_with_no_goals():
    goals = Goal.query.all()
    goals_response = [goal.g_json() for goal in goals]

    return jsonify(goals_response), 200

# Get one goal
@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)
    return jsonify({"goal":goal.g_json()}), 200

# Get tasks with no tasks & with no goal
@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_tasks_with_no_tasks(id):
    goal = validate_goal(id)
    goal_task = [Task.to_json(goal) for goal in goal.tasks]
    return jsonify({"id":goal.id, "title":goal.title, "tasks":goal_task}), 200

# Creat a goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.create(request_body)
    except KeyError:
        return make_response({"details":"Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.g_json()}), 201

# Update a goal
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()
    goal.update(request_body)

    db.session.commit()

    return jsonify({"goal":goal.g_json()}), 200

# Delete a goal
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)
    db.session.delete(goal)
    db.session.commit()


    return jsonify({"details": f'Goal {id} "{goal.title}" successfully deleted'}), 200

# Add tasks to a goal
@goals_bp.route("/<id>/tasks", methods=["POST"])
def add_task_to_goal(id): # we get id from the URL 
    goal = validate_goal(id) # we look up that validate_goal

    request_body = request.get_json() # turninig back the request to the dict.
    for task_id in request_body["task_ids"]: 
        task = validate_task(task_id)
        goal.tasks.append(task) # tasks is attributes of the goal 
       
    db.session.commit()

    return jsonify({
        "id": goal.id,
        "task_ids": request_body["task_ids"]
    }), 200

