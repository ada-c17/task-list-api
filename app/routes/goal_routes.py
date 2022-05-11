from app import db
from app.models.goal import Goal
from app.models.task import Task 
from .routes_helpers import validate_id, error_message
from flask import Blueprint, request, make_response, jsonify, abort

goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

# Get all goals
@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all() 
    goals_response = [goal.to_json() for goal in goals]
    return make_response(jsonify(goals_response), 200)

# Get one goal
@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_id("Goal", id)
    response_body = {}
    response_body["goal"] = goal.to_json()
    
    return make_response(jsonify(response_body), 200)

# Create a goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        message = "Invalid data"
        return error_message(message, 400)

    db.session.add(new_goal)
    db.session.commit()

    response_body = {}
    response_body["goal"] = new_goal.to_json()

    return make_response(jsonify(response_body), 201)

# Update a goal
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_id("Goal", id)
    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
    except KeyError:
        message = "Invalid data"
        return error_message(message, 400)

    db.session.commit()
    
    response_body = {}
    response_body["goal"] = goal.to_json()
    
    return make_response(jsonify(response_body), 200)

# Delete a goal
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_id("Goal", id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({'details':f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200)

# Post Task IDs to a GOAL
@goals_bp.route("/<id>/tasks", methods=["POST"])
def post_existing_tasks_to_goal(id):
    goal = validate_id("Goal", id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        validate_id("Task", task_id)
        task = Task.query.get(task_id)
        task.goal_id = goal.id
    
    db.session.commit()
    
    response_body = {}
    response_body = {
            "id":goal.id,
            "task_ids": request_body["task_ids"]}
    
    return make_response(jsonify(response_body), 200)

# Get tasks for one specific goal
@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_all_tasks_by_goal(id):
    goal = validate_id("Goal", id)
    
    tasks_response = [task.to_json() for task in goal.tasks]
    
    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }

    return make_response(jsonify(response_body), 200)
