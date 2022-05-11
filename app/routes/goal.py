from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal_or_abort(goal_id):
    # returns 400 error if invalid goal_id (alpha/non-int) 
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"error": f"{goal_id} is an invalid goal id"}, 400))
    
    # returns 404 error if goal_id not found in database
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"error": f"Goal {goal_id} not found"}, 404))
    return goal


@goals_bp.route("", methods=["GET"])
def get_saved_goals():
    goals = Goal.query.all()

    goal_list = []
    for goal in goals:
        goal_list.append(goal.return_goal_dict())
    
    return jsonify(goal_list), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_saved_goal(goal_id):
    goal = validate_goal_or_abort(goal_id)

    return jsonify({"goal": goal.return_goal_dict()}), 200


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    new_goal = Goal(title = request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.return_goal_dict()}), 201


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_saved_goal(goal_id):
    goal = validate_goal_or_abort(goal_id)
    
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return jsonify({"goal": goal.return_goal_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal_or_abort(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200