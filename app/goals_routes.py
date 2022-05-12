import os
from os import abort
from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime, timezone
import requests 
from dotenv import load_dotenv

load_dotenv()

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"Message":f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"Message":f"Goal {goal_id} not found"}, 404))

    return goal

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    response_body = []
    goals = Goal.query.all()

    for goal in goals: 
        response = goal.make_goal_dict()
        response_body.append(response)
    return jsonify(response_body), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    goal_dict = {"goal": goal.make_goal_dict()}
    return jsonify(goal_dict), 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    goal_dict = {"goal": new_goal.make_goal_dict()}

    return jsonify(goal_dict), 201

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    goal_dict = {"goal": goal.make_goal_dict()}

    return jsonify(goal_dict), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200