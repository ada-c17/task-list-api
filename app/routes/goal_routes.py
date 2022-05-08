from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.goal import Goal
from .helpers import validate_goal

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if request_body.get("title"):
        new_goal = Goal.create(request_body)
    else:
        abort(make_response({"details": "Invalid data"}, 400))
    
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_json()}), 201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goal_response_body = []
    for goal in goals:
        goal_response_body.append(goal.to_json())

    return jsonify(goal_response_body), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return jsonify({"goal": goal.to_json()}), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    if request_body.get("title"):
        goal.update(request_body)
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.commit()
    
    return jsonify({"goal": goal.to_json()}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\""\
                        " successfully deleted"}), 200