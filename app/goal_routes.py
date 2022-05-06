from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request
from .helpers import validate_goal, validate_task


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# POST ROUTES


@goals_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_goal = Goal.create(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_json()}, 201)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    if "task_ids" not in request_body:
        return make_response("Invalid Request", 400)
    for id in request_body["task_ids"]:
        task = validate_task(id)
        goal.tasks.append(task)

    db.session.commit()

    return make_response({"id": goal.goal_id, "task_ids": [task.task_id for task in goal.tasks]}, 200)

# GET ROUTES


@ goals_bp.route("", methods=["GET"])
def read_all_goals():
    sort_order = request.args.get("sort")

    if sort_order == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif sort_order == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()

    response = [goal.to_json() for goal in goals]

    return jsonify(response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return make_response({"goal": goal.to_json()}, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal(goal_id):
    goal = validate_goal(goal_id)
    tasks = Task.query.filter_by(goal=goal)
    tasks_response = [task.to_json() for task in tasks]
    return make_response({"id": goal.goal_id, "title": goal.title, "tasks": tasks_response}, 200)

# PUT ROUTES


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.update(request_body)

    db.session.commit()

    return make_response({"goal": goal.to_json()}, 200)

# DELETE ROUTES


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200)
