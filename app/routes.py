import os
import requests
from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return jsonify(
            {
                "details": "Invalid data"
            }), 400
    else:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body.get("completed_at"))

    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}
    return response_body, 201


def validate_and_return_item(cls, item_id):
    try:
        item_id = int(item_id)
    except:
        abort(make_response(jsonify({"details": "Invalid data"}, 400)))
    item = cls.query.get(item_id)
    if item:
        return item
    abort(make_response({"details": "Item not found"}, 404))


def update_completed_at(task, completed_at):
    task.completed_at = completed_at
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args
    if "sort" in params:
        if params["sort"] == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif params["sort"] == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        else:
            return make_response(jsonify(
                {"msg": "Please enter 'asc' or 'desc' parameter to sorting"}),
                400)
    else:
        tasks = Task.query.all()

    response = []

    for task in tasks:
        response.append(task.to_dict())
    return jsonify(response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_and_return_item(Task, task_id)
    return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_and_return_item(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_and_return_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify(
        {"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200


def send_notification(title):
    message = f'Someone just completed the task {title}'
    query = {"channel": "task-notifications", "text": f'"{message}"'}
    headers = {"Authorization": os.environ.get("SLACK_TOKEN")}
    requests.get("https://slack.com/api/chat.postMessage", headers=headers, params=query)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_completed_at_attribute(task_id):
    task = validate_and_return_item(Task, task_id)
    response = update_completed_at(task, datetime.utcnow())
    send_notification(task.title)
    return response


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_incompleted_tasks(task_id):
    task = validate_and_return_item(Task, task_id)
    return update_completed_at(task, None)


@goals_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify(
            {
                "details": "Invalid data"
            }), 400
    else:
        new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal.to_dict()}
    return response_body, 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response = []
    for goal in goals:
        response.append(goal.to_dict())
    return jsonify(response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_and_return_item(Goal, goal_id)
    return jsonify({"goal": goal.to_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_and_return_item(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_and_return_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify(
        {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_tasks_to_one_goal(goal_id):
    goal = validate_and_return_item(Goal, goal_id)
    request_body = request.get_json()
    try:
        task_ids = request_body["task_ids"]
    except KeyError:
        return jsonify({"msg": "Missing task_ids"}), 400

    if not isinstance(task_ids, list):
        return jsonify({"mgs": "Expected list of task ids"}), 400

    tasks = []
    for id in task_ids:
        task = Task.query.get(id)
        tasks.append(task)

    for task in tasks:
        task.goal_id = goal_id

    db.session.commit()

    return jsonify({
        "id": goal.goal_id,
        "task_ids": task_ids}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
    goal = validate_and_return_item(Goal, goal_id)

    tasks = []
    for task in goal.tasks:
        tasks.append(task.to_dict())
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks}), 200
