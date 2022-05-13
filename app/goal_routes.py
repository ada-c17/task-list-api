
from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
import os
from app.tasks_routes import validate_task_id

goals_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


def validate_goal_id(id):
    try:
        id = int(id)
    except:
        abort(make_response(
            {"message": f"goal {id} invalid.  Must be numerical"}, 400))

    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message": f"Goal {id} not found"}, 404))

    return goal


@goals_bp.route("", methods=["GET"])
def get_goals():
    title_query = request.args.get("title")
    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    else:
        goals = Goal.query.all()
    print(goals)
    goal_response = []
    for goal in goals:
        goal_response.append({
            "id": goal.id,
            "title": goal.title})
    return jsonify(goal_response)


@goals_bp.route("/<id>", methods=["GET"])
def get_single_goal(id):
    goal = validate_goal_id(id)
    return{"goal": {
        "id": goal.id,
        "title": goal.title}}


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": {
        "id": new_goal.id,
        "title": new_goal.title}}), 201)


@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    found_goal = validate_goal_id(id)

    request_body = request.get_json()

    found_goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal":
                    {"id": found_goal.id,
                     "title": found_goal.title}})


@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    found_goal = validate_goal_id(id)

    db.session.delete(found_goal)
    db.session.commit()

    return make_response(jsonify({"details": f'Goal {found_goal.id} "{found_goal.title}" successfully deleted'}))


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    tasks = []
    for id in task_ids:
        tasks.append(validate_task_id(id))
    for task in tasks:
        task.goal_id = goal.id

    db.session.commit()
    return jsonify({"id": goal.id,
                    "task_ids": task_ids})


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks(goal_id):
    goal = validate_goal_id(goal_id)
    tasks = []

    for task in goal.tasks:
        tasks.append(({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)}))
        if task.goal_id:
            tasks[-1]["goal_id"] = task.goal_id

    return jsonify({"id": goal.id,
                    "title": goal.title,
                    "tasks": tasks})
