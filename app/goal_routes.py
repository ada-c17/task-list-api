
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.helper_functions import *
import datetime as dt
from datetime import date
import os
import requests

goal_bp = Blueprint("Goals", __name__, url_prefix="/goals")

# Route functions

@goal_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = request.get_json()
    new_goal = create_record_safely(Goal, request_body)

    db.session.add(new_goal)
    db.session.commit()

    return success_message(dict(goal=new_goal.self_to_dict_no_tasks()), 201)

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    sort_param = request.args.get("sort")
    goals = Goal.query.all()
    all_goals = [goal.self_to_dict_no_tasks() for goal in goals]
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
    goal = get_record_by_id(Goal, goal_id)

    return return_database_info_dict("goal", goal.self_to_dict_no_tasks())

@goal_bp.route("/<goal_id>", methods=["PUT", "PATCH"])
def update_goal_by_id(goal_id):
    goal = get_record_by_id(Goal, goal_id)

    request_body = request.get_json()
    update_record_safely(Goal, goal, request_body)

    db.session.commit()

    return return_database_info_dict("goal", goal.self_to_dict_no_tasks())


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_record_by_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return success_message(dict(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted'))



# Join Routes

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = get_record_by_id(Goal, goal_id)
    request_body = request.get_json()

    for elem in request_body["task_ids"]:
        task = get_record_by_id(Task, elem)
        goal.tasks.append(task)

    db.session.commit()

    return return_database_info_list(goal.id_and_task_ids_only())

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_with_tasks(goal_id):
    goal = get_record_by_id(Goal, goal_id)

    return return_database_info_list(goal.self_to_dict_with_tasks())

