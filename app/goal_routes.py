from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.goal import Goal
from app.models.task import Task

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal is None:
        abort(make_response(jsonify(f"Goal {goal_id} not found"), 404))

    return goal

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return jsonify({"goal": goal.to_dict()}), 200


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201  


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()
    
    return jsonify({"goal": goal.to_dict()}), 200     


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    response = {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }

    return jsonify(response), 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks(goal_id):
    goal = validate_goal(goal_id)
    
    goal_dict = goal.to_dict()
    goal_dict["tasks"] = []
    for task in goal.tasks:
        task_dict = task.to_dict()
        task_dict["goal_id"] = task.goal_id
        goal_dict["tasks"].append(task_dict)

    return jsonify(goal_dict), 200


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks(goal_id):
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal_id
        db.session.add(task)
        db.session.commit()

    return jsonify({"id": int(goal_id), "task_ids": request_body["task_ids"]}), 200
       








