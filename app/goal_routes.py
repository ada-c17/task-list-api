from flask import Blueprint, jsonify, request, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db
from app.helper import validate_id

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", strict_slashes=False, methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    response = [goal.todict() for goal in goals]
    return jsonify(response), 200


@goal_bp.route("", strict_slashes=False, methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        abort(make_response({"details": f"Invalid data"}, 400))
    
    db.session.add(new_goal)
    db.session.commit()

    response = {"goal":new_goal.todict()}
    return jsonify(response), 201


@goal_bp.route("/<goal_id>", strict_slashes=False, methods=["GET"])
def get_goal(goal_id):
    goal = validate_id(Goal,goal_id)
    response = {"goal": goal.todict()}
    return jsonify(response), 200


@goal_bp.route("/<goal_id>", strict_slashes=False, methods=["PUT"])
def update_goal(goal_id):
    request_body = request.get_json()
    goal = validate_id(Goal,goal_id)
    goal.title = request_body["title"]
    response = {"goal":goal.todict()}
    return jsonify(response), 200


@goal_bp.route("/<goal_id>", strict_slashes=False, methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    response = { "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}
    db.session.delete(goal)
    db.session.commit()
    return jsonify(response), 200


@goal_bp.route("/<goal_id>/tasks", strict_slashes=False,methods=["POST"])
def add_task_list(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal_id

    db.session.commit()

    return {"id": goal.goal_id,
            "task_ids": [task.task_id for task in goal.tasks]}

@goal_bp.route("/<goal_id>/tasks", strict_slashes=False,methods=["GET"])
def get_goal_tasks(goal_id)
# @goal_bp.route("/<goal_id>/tasks", strickt_slashes=False,methods=["POST"])
# def create_task_on_goal(goal_id):
#     goal = validate_id(Goal, goal_id)
#     request_body = request.get_json()
#     new_task = Task.fromdict(request_body)
#     new_task.goal_id = goal.goal_id

#     db.session.add(new_task)
#     db.session.commit()


