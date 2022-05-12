from flask import Blueprint, request, make_response, abort, jsonify
import requests
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import date
import os
import requests
from app.routes.helper_routes import validate_id, validate_request

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = validate_request(request)
    new_goal = Goal(
        title=request_body["title"]
    )
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal": new_goal.to_dict()}, 201)

# GET /goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    # Pull query parameters from url
    title_param = request.args.get("title")
    # start the query
    goals = Goal.query
    # build up the search criteria based on params present
    if title_param:
        goals = goals.filter_by(title=title_param)
    # execute the search and return all records that meet the criteria built
    goals = goals.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

# GET /<goal_id>
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_id(goal_id)
    return {"goal": goal.to_dict()}

# PUT /<goal_id>
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_id(goal_id)
    # goal = Goal.query.get(goal_id)
    request_body = validate_request(request)
    goal.title = request_body["title"]
    db.session.commit()
    return make_response(jsonify({"goal": goal.to_dict()}))

# DELETE /<goal_id>
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'})

# Gather all tasks of one goal
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_one_goal(goal_id):
    goal = validate_id(goal_id)
    # request_body = validate_request(request)
    response = goal.to_dict()
    response["tasks"] = goal.get_tasks()
    return make_response(response)

# Gather all tasks of one goal
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def connect_tasks_to_goal(goal_id):
    goal = validate_id(goal_id)
    request_body = validate_request(request)
    for task_id in request_body["task_ids"]:
        goal.tasks.append(Task.query.get(task_id))
    db.session.commit()
    response = {"id": goal.goal_id, "task_ids": goal.get_task_ids()}
    return make_response(response)
