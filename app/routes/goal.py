
from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.goal import Goal
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
        "id": goal.goals_id,
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
        "id": goal.goals_id,
        "title": goal.title
        }

    return jsonify({"goal": response}), 200


@goals_bp.route("/<goals_id>", methods=["PUT"])
def update_goal(goals_id):
    goal = validate_goal(goals_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response = {
        "id": goal.goals_id,
        "title": goal.title,
        }

    return make_response({"goal": response})

@goals_bp.route("/<goals_id>", methods=["DELETE"])
def delete_goal(goals_id):
    goal = validate_goal(goals_id)

    db.session.delete(goal)
    db.session.commit()

    response = {
    "details": f"goal {goal.goals_id} \"{goal.title}\" successfully deleted"
    }

    return jsonify(response), 200
