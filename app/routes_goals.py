from flask import Blueprint, jsonify, request, abort, make_response
from .routes_tasks import validate_task
from app.models.goal import Goal
from app import db

goals_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response = {"details": f"{goal_id} is not valid input."}
        abort(make_response(jsonify(response), 400))
    
    goal = Goal.query.get(goal_id)

    if not goal:
        response = {"details": f"Goal {goal_id} does not exist."}
        abort(make_response(jsonify(response), 404))
    
    return goal

@goals_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response), 400))
    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }
    return jsonify(response), 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    
    response = []
    for goal in goals:
        response.append(goal.to_dict())
    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    response = {
        "goal": goal.to_dict()
    }
    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
        db.session.commit()
    except:
        response = {"details": "Goal needs a title"}
        abort(make_response(jsonify(response), 400))

    response = {
        "goal": goal.to_dict()
    }
    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_route(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}
    return jsonify(response), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_ids_for_tasks(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    for id in request_body["task_ids"]:
        task = validate_task(id) # this checks, add test
        task.goal_id = goal.goal_id
    db.session.commit()

    response = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"] # is this the best way?
    }

    return jsonify(response), 200

@goals_bp.route("/<goal_id>/tasks")
def get_tasks_for_one_goal(goal_id):
    goal = validate_goal(goal_id)

    goal_tasks = goal.tasks

    response = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []
    }

    for task in goal_tasks:
        response["tasks"].append({
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })

    return jsonify(response), 200