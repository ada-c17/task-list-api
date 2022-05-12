from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.utils.helper import get_or_abort, get_JSON_request_body
from flask import Blueprint, jsonify, abort, make_response, request


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["GET"])
def read_all_goals():

    title_query = request.args.get("sort")
    if title_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    elif title_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    else:
        goals = Goal.query

    goals_response = [goal.to_JSON_response()["goal"] for goal in goals]

    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):

    goal = get_or_abort(Goal, goal_id)

    return jsonify(goal.to_JSON_response()), 200


@goals_bp.route("", methods=["POST"])
def create_goal():

    new_goal = Goal.from_JSON_request()

    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.to_JSON_response()), 201


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    goal = get_or_abort(Goal, goal_id)
    goal.update_from_JSON_request()

    db.session.commit()

    return jsonify(goal.to_JSON_response()["goal"]), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

    goal = get_or_abort(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_a_goal(goal_id):

    goal = get_or_abort(Goal, goal_id)

    payload = get_JSON_request_body(request)

    if "task_ids" not in payload:
        return jsonify({"details": "Invalid data"}), 400

    for task_id in payload["task_ids"]:
        task = get_or_abort(Task, task_id)
        task.goal_id = goal_id

    db.session.commit()

    rsp = {
        "id": goal.goal_id,
        "task_ids": payload["task_ids"]
    }

    return jsonify(rsp), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):

    goal = get_or_abort(Goal, goal_id)

    payload = goal.to_JSON_response()["goal"]
    tasks = [task.to_JSON_response()["task"] for task in goal.tasks]
    payload["tasks"] = tasks

    return jsonify(payload), 200
