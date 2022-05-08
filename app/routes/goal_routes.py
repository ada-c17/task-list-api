from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.goal import Goal
# from sqlalchemy import desc
# import requests
# import os

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def make_goal_safely(data_dict):
    try:
        return Goal.from_dict(data_dict)
    except KeyError as err:
        error_message(f"Invalid data", 400)

def update_goal_safely(goal, data_dict):
    try:
        return goal.replace_details(data_dict)
    except KeyError as err:
        error_message(f"Invalid data", 400)

def validate_goal_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)
    goal = Goal.query.get(id)
    if goal:
        return goal
    error_message(f"No goal with ID {id}. SORRY.", 404)

@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    new_goal=make_goal_safely(request_body)

    db.session.add(new_goal)
    db.session.commit()

    task_response = {"goal":new_goal.to_dict()}

    return jsonify(task_response), 201

@goal_bp.route("", methods=["GET"])
def get_goals():
#     sort_param = request.args.get("sort")
#     if sort_param == "asc":
#         tasks = Task.query.order_by("title")
#     elif sort_param == "desc":
#         tasks = Task.query.order_by(desc(Task.title))
#     else:
    goals = Goal.query.all()

    result_list = [goal.to_dict() for goal in goals]
    return jsonify(result_list)

@goal_bp.route("/<id>", methods=["GET"])
def get_goal_by_id(id):
    goal = validate_goal_id(id)
    result = {"goal": goal.to_dict()}
    return jsonify(result)

@goal_bp.route("<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal_id(id)
    request_body = request.get_json()
    updated_goal = update_goal_safely(goal, request_body)

    db.session.commit()

    return jsonify({"goal":updated_goal})

@goal_bp.route("<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal_id(id)
    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details":f'Goal {id} "{goal.title}" successfully deleted'})

# @task_bp.route("<id>/mark_complete", methods=["PATCH"])
# def mark_complete(id):
#     task = validate_task_id(id)
#     updated_task = task.mark_done()

#     db.session.commit()
#     send_slack_message(f"Someone just completed the task {task.title}")

#     return jsonify({"task":updated_task})

# @task_bp.route("<id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(id):
#     task = validate_task_id(id)
#     updated_task = task.mark_not_done()

#     db.session.commit()

#     return jsonify({"task":updated_task})

# def send_slack_message(message):
#     Slack_Key = os.environ.get("Slack_API_Token")
#     requests.post('https://slack.com/api/chat.postMessage', params={'text':message, 'channel':'task-notifications'}, headers={'Authorization':Slack_Key})
#     return True