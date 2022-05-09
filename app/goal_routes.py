
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
import datetime as dt
from datetime import date
import os
import requests

goal_bp = Blueprint("Goals", __name__, url_prefix="/goals")

# Helper functions

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def success_message(message, status_code=200):
    return make_response(jsonify(message), status_code)

def return_database_info_list(return_value):
    return make_response(jsonify(return_value))

def return_database_info_goal(return_value):
    return make_response(jsonify(dict(goal=return_value)))

def get_goal_by_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id: {id}", 400)
    goal = Goal.query.get(id)
    if goal:
        return goal
    else:
        error_message(f"Goal id: {id} not found", 404)

def create_goal_safely(data_dict):
    try:
        return Goal.create_from_dict(data_dict)
    except ValueError as err:
        error_message(f"Invalid data", 400)
    except KeyError as err:
        error_message(f"Missing key(s): {err}.  Goal not added to Goal List.", 400)

def update_goal_safely(goal, data_dict):
    try:
        goal.update_self(data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}. Goal not updated.", 400)
    except KeyError as err:
        error_message(f"Missing key(s): {err}. Goal not updated.", 400)

# def send_slackbot_message(title):
#     path = "https://slack.com/api/chat.postMessage"
#     slackbot_key = os.environ.get("SLACK_OAUTH_TOKEN")
#     headers = {'authorization': 'Bearer ' + slackbot_key}
#     params = {
#         'channel' : 'goal-notifications',
#         'text' : f'Someone just completed goal {title}! :tada::tada::tada:',
#     }
#     requests.patch(path, headers=headers, params=params)



# Route functions

@goal_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = request.get_json()
    new_goal = create_goal_safely(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return success_message(dict(goal=new_goal.self_to_dict()), 201)

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    sort_param = request.args.get("sort")
    goals = Goal.query.all()
    all_goals = [goal.self_to_dict() for goal in goals]
    if not sort_param:
        return return_database_info_list(all_goals)
    if sort_param == "asc":
        sorted_goals_asc = sorted(all_goals, key = lambda i : i["title"])
        return return_database_info_list(sorted_goals_asc)
    if sort_param == "desc":
        sorted_goals_desc = sorted(all_goals, key = lambda i : i["title"], reverse=True)
        return return_database_info_list(sorted_goals_desc)


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = get_goal_by_id(goal_id)

    return return_database_info_goal(goal.self_to_dict())

@goal_bp.route("/<goal_id>", methods=["PUT", "PATCH"])
def update_goal_by_id(goal_id):
    goal = get_goal_by_id(goal_id)

    request_body = request.get_json()
    update_goal_safely(goal, request_body)

    db.session.commit()

    return return_database_info_goal(goal.self_to_dict())

# @goal_bp.route("/<goal_id>/<completion_status>", methods=["PATCH"])
# def update_goal_completion_status(goal_id, completion_status):
#     goal = get_goal_by_id(goal_id)

#     if completion_status == "mark_complete":
#         completion_info = {
#             "completed_at" : dt.date.today()
#         }
#         update_goal_safely(goal, completion_info)
#         send_slackbot_message(goal.title)
#     elif completion_status == "mark_incomplete":
#         completion_info = {
#             "completed_at" : None
#         }
#         update_goal_safely(goal, completion_info)

#     db.session.commit()

#     return return_database_info_goal(goal.self_to_dict())


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_goal_by_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return success_message(dict(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted'))