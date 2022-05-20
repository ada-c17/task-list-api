from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from .routes_helper import get_record_by_id, abort_message
from app import db


bp = Blueprint("goals", __name__, url_prefix="/goals")


@bp.route("", methods=("POST",))
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        abort_message("Missing title", 400)

    goal = Goal.from_dict(request_body)
    db.session.add(goal)
    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 201)


@bp.route("/<goal_id>/tasks", methods=("POST",))
def add_tasks_to_goal(goal_id):
    goal = get_record_by_id(goal_id)
    request_body = request.get_json()

    tasks_list = []
    for task_id in request_body["task_ids"]:
        task = get_record_by_id(task_id)
        task.goal = goal
        tasks_list.append(task.task_id)

    db.session.commit()
    return make_response(jsonify({"id": goal.goal_id, 
    "task_ids": tasks_list}))
    

@bp.route("/<goal_id>", methods=("GET",))
def read_goal(goal_id):
    goal = get_record_by_id(goal_id)
    return make_response(jsonify({"goal": goal.to_dict()}))


@bp.route("", methods=("GET",))
def read_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    return make_response(jsonify(goals_response))


@bp.route("/<goal_id>/tasks", methods=("GET",))
def read_specific_goal_tasks(goal_id):
    goal = get_record_by_id(goal_id)
    
    goal_tasks = [Task.to_dict(task) for task in goal.tasks]

    return make_response(jsonify({
        "id": goal.goal_id, 
        "title": goal.title, 
        "tasks": goal_tasks})
    )
    

@bp.route("/<goal_id>", methods=("PUT",))
def replace_goal(goal_id):
    goal = get_record_by_id(Goal, goal_id)
    request_body = request.get_json()
    if "title" not in request_body:
        abort_message("Title not found", 404)
    goal.override_goal(request_body)
    db.session.commit()

    return jsonify({"goal": goal.to_dict()})


@bp.route("/<goal_id>", methods=("DELETE",))
def delete_goal(goal_id):
    goal = get_record_by_id(goal_id)
    db.session.delete(goal)
    db.session.commit()

    abort_message(f'Goal {goal_id} "{goal.title}" successfully deleted')