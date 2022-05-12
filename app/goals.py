from crypt import methods
from datetime import datetime
from turtle import title
from flask import Blueprint, jsonify, request, abort, make_response
from pytest import param
from app import db
from app.models.goal import Goal
import requests


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# helper functions
def get_goal_or_abort(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        rsp = {"msg":f"Invalid id {goal_id}"}
        abort(make_response(jsonify(rsp), 400))

    goal = Goal.query.get(goal_id)
    if goal is None:
        rsp = {"msg":f"Could not find goal with id {goal_id}"}
        abort(make_response(jsonify(rsp), 404))
    return goal

def to_dict(goal):
    return {
        "id": goal.goal_id,
        "title": goal.title
    }

# routes
@goals_bp.route("", methods=['POST'])
def create_one_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title = request_body["title"])
    except KeyError:
        return { "details": "Invalid data"}, 400
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(
        {
            "goal": to_dict(new_goal)
        }
    ),201

@goals_bp.route("", methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(to_dict(goal))

    return jsonify(goals_response), 200


@goals_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    goal = get_goal_or_abort(goal_id)
    return jsonify(
        {
            "goal": to_dict(goal)
        }
    ), 200


@goals_bp.route('/<goal_id>', methods=['PUT'])
def update_goal(goal_id):
    goal = get_goal_or_abort(goal_id)
    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
    except KeyError:
        return {
            "msg": "title are required" 
        }, 400
    
    db.session.commit()
    return jsonify(
        {
            "goal": to_dict(goal)
        }
    ), 200


@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_one_goal(goal_id):
    goal = get_goal_or_abort(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }, 200