from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from sqlalchemy import desc
from app.routes.helper import validate

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(
            title=request_body["title"]
        )
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)
    
    db.session.add(new_goal)
    db.session.commit()
    response_body = {
        "goal": new_goal.return_goal_dict()
    }

    return make_response(jsonify(response_body), 201)

@goal_bp.route("", methods=["GET"])
def get_goals():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "desc":
            goals = Goal.query.order_by(desc(Goal.title))
        elif sort_query == "asc":
            goals = Goal.query.order_by(Goal.title)
    else:
        goals = Goal.query.all()
    response = []
    for goal in goals:
        response.append(goal.return_goal_dict())
    return jsonify(response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate(Goal, goal_id)
    response = {
        "goal": goal.return_goal_dict()
    }
    return jsonify(response)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response = {
        "goal": goal.return_goal_dict()
    }

    return make_response(jsonify(response), 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    response = {'details': f'Goal {goal_id} "{goal.title}" successfully deleted'}

    return make_response(jsonify(response), 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate(Goal, goal_id)

    request_body = request.get_json()
    try:
        task_ids = request_body["task_ids"]
    except KeyError:
        return jsonify({'msg': "Missing task_ids in request body"}), 400

    if not isinstance(task_ids, list):
        return jsonify({'msg': "Expected list of task ids"}), 400
    
    tasks = []
    for id in task_ids:
        tasks.append(validate(Task, id))
    
    for task in tasks:
        task.goal = goal

    db.session.commit()

    response = {
        "id": goal.goal_id,
        "task_ids": task_ids
    }

    return make_response(jsonify(response), 200)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(
            {"id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }
        )
    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
    }

    return make_response(jsonify(response_body), 200)
    