from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from ..models.goal import Goal
from .task_routes import validate_task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


#helper function
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)
#check goal is found
    if not goal:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))
    else:
        return goal


#routes

@goals_bp.route("", methods=["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal(
            title=request_body["title"]
            )
    except: 
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal.to_dict()}

    return make_response(jsonify(response_body), 201)


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]
    return make_response(jsonify(goals_response), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_goal(goal_id)

    response_body = {"goal": goal.to_dict()}

    return make_response(jsonify(response_body), 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
    except KeyError as err:
        return make_response(f"Key error {err}", 400)
    
    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return make_response(jsonify(response_body), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)
    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": [task.to_dict_with_goal() for task in goal.tasks]
    }

    return make_response(jsonify(response_body), 200)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    try:
        request_body = request.get_json()
        for task_id in request_body["task_ids"]:
            task = validate_task(task_id)
            task.goal_id = goal.goal_id
    except: 
        abort(make_response({"details": "Invalid data"}, 400))
    # db.session.add(new_goal)
    db.session.commit()

    response_body = {
        "id": goal.goal_id,
        "task_ids": [task.task_id for task in goal.tasks]}

    return make_response(jsonify(response_body), 200)

