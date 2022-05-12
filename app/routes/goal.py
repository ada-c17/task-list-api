from flask import Blueprint, jsonify, request
from app import db, helper_functions
from app.models.goal import Goal

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["GET"])
def get_saved_goals():
    goals = Goal.query.all()

    goal_list = []
    for goal in goals:
        goal_list.append(goal.return_goal_dict())
    
    return jsonify(goal_list), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_saved_goal(goal_id):
    goal = helper_functions.validate_goal_or_abort(goal_id)

    return jsonify({"goal": goal.return_goal_dict()}), 200


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal(title = request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.return_goal_dict()}), 201


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_saved_goal(goal_id):
    goal = helper_functions.validate_goal_or_abort(goal_id)
    
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return jsonify({"goal": goal.return_goal_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = helper_functions.validate_goal_or_abort(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = helper_functions.validate_goal_or_abort(goal_id)

    request_body = request.get_json()

    tasks_to_assign = []
    task_ids = request_body["task_ids"]
    for id in task_ids:
        tasks_to_assign.append(helper_functions.validate_task_or_abort(id))

    for task in tasks_to_assign:
        task.goal = goal
    
    db.session.commit()

    response = {
        "id": goal.goal_id,
        "task_ids": task_ids
    }

    return jsonify(response), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = helper_functions.validate_goal_or_abort(goal_id)

    tasks_for_goal = []
    for task in goal.tasks:
        tasks_for_goal.append(
            {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }
        )

    response = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_for_goal
    }

    return jsonify(response), 200