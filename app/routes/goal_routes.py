from flask import Blueprint, jsonify, make_response, request, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db
import datetime
import os

goals_bp = Blueprint("goals",__name__,url_prefix="/goals")

@goals_bp.route("",methods=["GET"])
def get_goals():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query.lower() == "asc":
            goals = Goal.query.order_by(Goal.title)
        elif sort_query.lower() == "desc":
            goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    response = []
    if goals:
        for goal in goals:
            response.append(goal.to_json(goal=False))
    return make_response(jsonify(response),200)

@goals_bp.route("",methods=["POST"])
def make_goal():
    request_body = request.get_json()
    new_goal = Goal.from_json(request_body)
    db.session.add(new_goal)
    db.session.commit()
    response = new_goal.to_json()
    return make_response(response,201)

@goals_bp.route("/<id>",methods=["GET"])
def get_goal(id):
    goal = Goal.validate_id(id)
    response = goal.to_json()
    return make_response(response,200)

@goals_bp.route("/<id>",methods=["PUT"])
def update_goal(id):
    goal = Goal.validate_id(id)
    request_body = request.get_json()
    try:
        goal.title = request_body["title"]
    except KeyError:
        return make_response({"details":"Incomplete data"},400)
    db.session.commit()
    response = goal.to_json()
    return make_response(response,200)

@goals_bp.route("/<id>",methods=["DELETE"])
def delete_goal(id):
    goal = Goal.validate_id(id)
    db.session.delete(goal)
    db.session.commit()
    return make_response({"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"},200)

@goals_bp.route("/<id>/tasks",methods=["POST"])
def assign_tasks(id):
    goal = Goal.validate_id(id)
    request_body = request.get_json()
    if request_body.get("task_ids",None):
        for task_id in request_body.get("task_ids"):
            task = Task.validate_id(task_id)
            task.goal_id = id
        db.session.commit()
    return make_response({"id":goal.goal_id,"task_ids":request_body.get("task_ids")},200)

@goals_bp.route("/<id>/tasks",methods=["GET"])
def get_goal_tasks(id):
    goal = Goal.validate_id(id)
    tasks = [task.to_json(task=False) for task in goal.tasks]
    response = goal.to_json(goal=False)
    response["tasks"] = tasks
    return make_response(response,200)