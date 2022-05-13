from flask import Blueprint, jsonify, make_response, request
# from app.models.task import Task
from app.models.goal import Goal
from .routes_helper import validate_goal_id, create_message, validate_task_id
from app import db


bp = Blueprint("goals", __name__, url_prefix="/goals")


@bp.route("", methods=("POST",))
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        create_message("Invalid data", 400)

    goal = Goal.from_dict(request_body)
    db.session.add(goal)
    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 201)


@bp.route("/<goal_id>/tasks", methods=("POST",))
def add_tasks_to_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()

    tasks_list = []
    for task_id in request_body["task_ids"]:
        task = validate_task_id(task_id)
        task.goal = goal
        tasks_list.append(task.task_id)

    db.session.commit()
    return make_response(jsonify({"id": goal.goal_id, "task_ids": tasks_list}))
    

@bp.route("/<goal_id>", methods=("GET",))
def read_goal(goal_id):
    goal = validate_goal_id(goal_id)
    return make_response(jsonify({"goal": goal.to_dict()}), 200)


@bp.route("", methods=("GET",))
def read_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    return make_response(jsonify(goals_response), 200)


@bp.route("/<goal_id>", methods=("PUT",))
def replace_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    goal.override_goal(request_body)
    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200


@bp.route("/<goal_id>", methods=("DELETE",))
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)
    db.session.delete(goal)
    db.session.commit()

    create_message(f'Goal {goal_id} "{goal.title}" successfully deleted', 200)