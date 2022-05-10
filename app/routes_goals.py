from flask import Blueprint, jsonify, request, abort, make_response
from .models.task import Task
from .models.goal import Goal
from app import db
import os
import requests

goal_bp = Blueprint("", __name__, url_prefix="/goals" )


# helper function:
def validate_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"message":f"task {goal_id} not found"}, 404))
    return goal

# CREATE (CRUD)
# POST request to /goals
# request_body = {"title": "My New Goal"}

@goal_bp.route("", methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    new_goal = Goal(title=request_body['title'])
    db.session.add(new_goal)
    db.session.commit()
    response = {
        "goal": 
        {"id": new_goal.goal_id,
        "title": new_goal.title}
        }
    return jsonify(response), 201


# READ (CRUD): aka GET
@goal_bp.route("", methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    goal_list = []
    for goal in goals:
        goal_list.append( {
            "id": goal.goal_id,
            "title": goal.title
        })
    return jsonify(goal_list), 200

@goal_bp.route("/<goal_id>",methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_goal(goal_id)
    response = { 'goal':
            {"id": goal.goal_id,
            "title": goal.title}
            }
    return jsonify(response), 200

# UPDATE(CRUD): aka PATCH/PUT
@goal_bp.route("/<goal_id>",methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body['title']
    db.session.commit()

    response = {
        "goal": {
            "goal_id": goal.goal_id,
            "title": goal.title,
        }
    }
    return jsonify(response), 200

# DELETE (CRUD)