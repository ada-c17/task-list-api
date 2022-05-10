from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.goal import Goal
from datetime import datetime

goals_bp = Blueprint("goals", __name__, url_prefix='/goals')

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"msg": f"Invalid Id: '{goal_id}'. ID must be an integer"}, 400))

    chosen_goal = Goal.query.get(goal_id)

    if not chosen_goal:
        abort(make_response({"msg": f"Goal {goal_id} not found"}, 404))

    return chosen_goal

@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():
    if request.method == "GET":
        goals = Goal.query.all()
        goals_response = []
        for goal in goals:
            goals_response.append(
                {
                    "id": goal.id,
                    "title": goal.title
                }
            )
        return jsonify(goals_response)

    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({
            "goal" :{
                "id": new_goal.id,
                "title": new_goal.title
            }
        }), 201

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)
    return jsonify({
        "goal": {
            "id": chosen_goal.id,
            "title": chosen_goal.title
        }
    })

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    request_body = request.get_json()
    chosen_goal = validate_goal(goal_id)

    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    chosen_goal.title = request_body["title"]

    db.session.commit()

    return jsonify({
        "goal": {
            "id": chosen_goal.id,
            "title": chosen_goal.title
        }
    })

    
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'})


