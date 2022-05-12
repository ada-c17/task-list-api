
from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.goal import Goal
from datetime import datetime
import os

goals_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response(
            {"message": f"goal {goal_id} invalid.  Must be numerical"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))

    return goal


@goals_bp.route("", methods=["GET"])
def get_goals():
    title_query = request.args.get("title")
    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    else:
        goals = Goal.query.all()
    print(goals)
    goal_response = []
    for goal in goals:
        goal_response.append({
            "id": goal.goal_id,
            "title": goal.title})
    return jsonify(goal_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_single_goal(goal_id):
    goal = validate_goal_id(goal_id)
    return{"goal": {
        "id": goal.goal_id,
        "title": goal.title}}


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title}}), 201)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    found_goal = validate_goal_id(goal_id)

    request_body = request.get_json()

    found_goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal":
                    {"id": found_goal.goal_id,
                     "title": found_goal.title}})


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    found_goal = validate_goal_id(goal_id)

    db.session.delete(found_goal)
    db.session.commit()

    return make_response(jsonify({"details": f'Goal {found_goal.goal_id} "{found_goal.title}" successfully deleted'}))
