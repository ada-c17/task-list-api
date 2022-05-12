from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from ..models.goal import Goal
from ..models.task import Task
from .routes_helper import success_response, error_response, validate_item

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal(
            title=request_body["title"]
            )
    except: 
        error_response({"details": "Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal.to_dict()}
    return success_response(response_body, 201)


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]
    
    return success_response(goals_response, 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_item(Goal, goal_id)

    response_body = {"goal": goal.to_dict()}

    return success_response(response_body, 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
    except KeyError as err:
        return make_response(f"Key error {err}", 400)
    
    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return success_response(response_body, 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return success_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks]
    }

    return success_response(response_body, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    try:
        request_body = request.get_json()
        for task_id in request_body["task_ids"]:
            task = validate_item(Task, task_id)
            task.goal_id = goal.goal_id
    except: 
        error_response({"details": "Invalid data"}, 400)

    db.session.commit()

    response_body = {
        "id": goal.goal_id,
        "task_ids": [task.task_id for task in goal.tasks]}

    return success_response(response_body, 200)

