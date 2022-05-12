from flask import Blueprint, abort, make_response,jsonify, request
import requests
from app import db
from app.models.task import Task
from app.models.goal import Goal
from .helper_functions import get_goal_record_by_id, get_task_record_by_id, update_goal_safely, update_task_safely

goals_bp = Blueprint("Goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError as err:
        abort(make_response(jsonify(dict(details=f"Invalid data")),400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify(goal=new_goal.self_to_dict()),201)

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = get_goal_record_by_id(id)

    request_body = request.get_json()

    update_goal_safely(goal, request_body)

    db.session.commit()

    return make_response(jsonify(goal=goal.self_to_dict()),201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response = [goal.self_to_dict() for goal in goals]
    return jsonify(response)

@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = get_goal_record_by_id(id)
    return jsonify(goal=goal.self_to_dict())

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):

    goal = get_goal_record_by_id(goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    update_dict = {"goal_id": goal.goal_id}
    for task_id in task_ids:
        task = get_task_record_by_id(task_id)
        update_task_safely(task, update_dict)
    db.session.commit()
    return make_response(jsonify({"id": goal.goal_id,"task_ids": task_ids}), 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal(goal_id):

    goal = get_goal_record_by_id(goal_id)
    tasks = Task.query.filter_by(goal_id=goal.goal_id)
    task_list = [task.self_to_dict() for task in tasks]
    response = {"id": goal.goal_id,
                "title": goal.title,
                "tasks": task_list}
    return jsonify(response)


@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = get_goal_record_by_id(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify(details=f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"),200)

