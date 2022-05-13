from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from .routes_helper import validate_goal_id, create_message
from app import db


bp = Blueprint("goals", __name__, url_prefix="/goals")


@bp.route("", methods=("POST",))
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        create_message("Invalid data", 400)

    goal = Goal.from_dict(request_body)
    db.session.add(goal)
    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 201)


@bp.route("/<goal_id>", methods=("GET",))
def read_goal(goal_id):
    goal = validate_goal_id(goal_id)
    return make_response(jsonify({"goal": goal.to_dict()}), 200)


@bp.route("", methods=("GET",))
def real_all_goals():
    goals = Goal.query.all()
    goals_response = [task.to_dict() for task in goals]
    return make_response(jsonify(goals_response), 200)


@bp.route("/<goal_id>", methods=("PUT",))
def replace_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    goal.override_goal(request_body)
    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200


@bp.route("/<goal_id>", methods=("DELETE",))
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)
    db.session.delete(goal)
    db.session.commit()

    create_message(f'Goal {goal_id} "{goal.title}" successfully deleted', 200)