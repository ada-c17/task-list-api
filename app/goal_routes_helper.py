from flask import abort, make_response, jsonify
from app.models.goal import Goal

def check_goal_exists(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(jsonify({"error": f"Goal {goal_id} does not exist"}), 404))
    
    return goal

def try_to_make_goal(response_body):
    try:
        return Goal.make_goal(response_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))


