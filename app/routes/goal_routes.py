from flask import Blueprint, jsonify, request, make_response, abort
from app.models.goal import Goal
from app import db

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    '''Validates that goal id is valid and exists'''
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"msg": f"Invalid id: {goal_id}"}, 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"msg": f"Could not find goal with id: {goal_id}"}, 404))
    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(
            title=request_body["title"] 
        )
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })
    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}