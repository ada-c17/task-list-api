
from app import db
from app.models.goal import Goal
from app.helper import validate_goal
from flask import Blueprint, request, jsonify, make_response

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

# POST
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body.keys():
        return {"details": "Invalid data"}, 400

    new_goal = Goal.create(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_json()}, 201

# GET all
@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())

    return jsonify(goals_response), 200

# GET one goal
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return { "goal": goal.to_json()}, 200

# UPDATE one goal
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.update(request_body)

    db.session.commit()

    return {"goal": goal.to_json()}, 200

# DELETE one goal
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()
    return make_response({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}), 200