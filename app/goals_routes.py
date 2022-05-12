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

def make_goal_dict(goal):
    goal_dict = {
            "id": goal.goal_id,
            "title": goal.title,
    }
    # if goal.completed_at:
    #     goal_dict["is_complete"] = True
    # else:
    #     goal_dict["is_complete"] = False

    return goal_dict

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    response_body = []
    goals = Goal.query.all()

    for goal in goals: 
        response = {
            "id": goal.goal_id,
            "title": goal.title
        }
        response_body.append(response)
    return jsonify(response_body), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    goal_dict = {"goal": make_goal_dict(goal)}
    return jsonify(goal_dict), 200