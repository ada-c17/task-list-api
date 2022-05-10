from app import db
from flask import Blueprint, jsonify, request, make_response
from app.models.goal import Goal
from .goal_routes_helper import try_to_make_goal, check_goal_exists

goals_bp = Blueprint("goals", __name__, url_prefix = "/goals")


# Create a Task
@goals_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = try_to_make_goal(request_body)

    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify({"goal": new_goal.to_json()}), 201

# Get Goals
@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_json() for goal in goals]

    return jsonify(goals_response), 200

# Get a single Goal
@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_task(goal_id):
    goal = check_goal_exists(goal_id)

    return make_response(jsonify({"goal": goal.to_json()}), 200)

# Update Task
@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_task(goal_id):
    goal = check_goal_exists(goal_id)
    request_body = request.get_json()

    goal.update_goal(request_body)
    db.session.commit()

    return make_response(jsonify({"goal": goal.to_json()}), 200)

# # Delete Task
# @goals_bp.route("/<goal_id>", methods = ["DELETE"])
# def delete_task(goal_id):
#     task = check_task_exists(goal_id)

#     db.session.delete(task)
#     db.session.commit()

#     return jsonify({"details": f'Task {task.goal_id} "{task.title}" successfully deleted'}), 200