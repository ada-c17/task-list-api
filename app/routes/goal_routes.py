from app import db
from app.models.goal import Goal
from flask import Blueprint, make_response, request, jsonify, abort
from .helpers import validate_goal
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

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()
    goal.update(request_body)

    db.session.commit()

    return jsonify({"goal":goal.g_json()}), 200

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)
    db.session.delete(goal)
    db.session.commit()


    return jsonify({"details": f'Goal {id} "{goal.title}" successfully deleted'}), 200