import os
from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, abort, make_response
import requests

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# Validate there is title when creating or updating a goal
def validate_create_or_put():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        rsp = {
            "details": "Invalid data"
        }
        abort(make_response(jsonify(rsp), 400))
    
    return new_goal


@goals_bp.route('', methods=['POST'])
def create_one_goal():
    new_goal = validate_create_or_put()
    
    db.session.add(new_goal)
    db.session.commit()
    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route('', methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    rsp = []
    
    for goal in goals:
        rsp.append(goal.to_dict())

    return jsonify(rsp), 200

def get_goal_or_abort(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {goal_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_goal = Goal.query.get(goal_id)
    if chosen_goal is None:
        rsp = {"msg": f"Could not find goal with id {goal_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_goal

@goals_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    chosen_goal = get_goal_or_abort(goal_id)

    rsp = {"goal": chosen_goal.to_dict()}
    return jsonify(rsp), 200

@goals_bp.route("/<goal_id>", methods=['PUT'])
def put_one_goal(goal_id):
    chosen_goal = get_goal_or_abort(goal_id)
    new_goal = validate_create_or_put()

    chosen_goal.title = new_goal.title
    
    db.session.commit()    
    
    rsp = {"goal": chosen_goal.to_dict()}
    return jsonify(rsp), 200

@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_one_goal(goal_id):
    chosen_goal = get_goal_or_abort(goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()
    rsp = {
        "details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'
    }
    return jsonify(rsp), 200