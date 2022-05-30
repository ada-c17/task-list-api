from datetime import date
from urllib import response
from flask import Blueprint, jsonify, make_response, abort, request
from app.models.goal import Goal
from app.models.task import Task
from app import db

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods = ["GET"])
def get_all_goal():
    goal_response_body = []

    if request.args.get("sort") == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif request.args.get("sort") == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()

    for goal in goals:
        goal_response_body.append(goal.to_json())

    return jsonify(goal_response_body), 200

@goal_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()
    print(request_body)
    
    try:
        new_goal = Goal.create(request_body)
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(new_goal)
    db.session.commit()

    response_body = {}
    response_body["goal"] = new_goal.to_json()
    return jsonify(response_body), 201

@goal_bp.route("/<id>", methods = ["GET"])
def get_one_goal(id):
    one_goal = Goal.validate(id)
    response_body = {}
    response_body["goal"] = one_goal.to_json()

    return jsonify(response_body), 200

@goal_bp.route("/<id>", methods = ["PUT"])
def update_goal(id):
    one_goal = Goal.validate(id)
    request_body = request.get_json()

    one_goal.update(request_body)

    db.session.commit()
    response_body = {}
    response_body["goal"] = one_goal.to_json()

    return jsonify(response_body), 200


@goal_bp.route("/<id>", methods = ["DELETE"])
def delete_goal(id):
    one_goal = Goal.validate(id)
    db.session.delete(one_goal)
    db.session.commit()

    return jsonify({"details": f'Goal {one_goal.goal_id} "{one_goal.title}" successfully deleted'})

@goal_bp.route("/<id>/tasks", methods = ["POST"])
def list_of_task_to_goal(id):
    valid_goal = Goal.validate(id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        Task.validate(task_id)
        task = Task.query.get(task_id)
        task.goal_id = valid_goal.goal_id

    db.session.commit()
    task_list = []

    for task in valid_goal.tasks:
        task_list.append(task.task_id)

    response_body = {}
    response_body = {
        "id": valid_goal.goal_id,
                    "task_ids": task_list}
    
    return jsonify(response_body), 200

@goal_bp.route("/<id>/tasks", methods = ["GET"])
def get_task_one_goal(id):
    valid_goal = Goal.validate(id)
    task_list = []

    for task in valid_goal.tasks:
        task_list.append(task.to_json())

    response_body = {}
    response_body = {
        "id": valid_goal.goal_id,
        "title": valid_goal.title,
        "tasks": task_list}
    
    return jsonify(response_body), 200



