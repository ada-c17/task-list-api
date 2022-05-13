from asyncio import Task
from flask import Blueprint
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import os
# from .helper import validate_planet

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response(jsonify(f"goal {goal_id} invalid"), 400))
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(jsonify(f"goal {goal_id} not found"), 404))
    return goal

@goal_bp.route("", methods=["POST"])
def create_goals():
    request_body = request.get_json()
    try:
        new_goal = Goal(title = request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
    except:
        abort(make_response({"details":f"Invalid data"}, 400))
    return make_response({"goal" : new_goal.to_json()}, 201)


@goal_bp.route("", methods=["GET"])
def read_all_goals():
    

    title_query = request.args.get("title")
    

    if title_query:
        goals = Goal.query.filter_by(Goal.title)
    else:
        goals = Goal.query.all()
    goals_response = []    
    try:
        for goal in goals:
            goals_response.append(goal.to_json())
            
    except:
        abort(make_response({"details":f"goal not found"}, 404))
    return make_response(jsonify(goals_response),200)




@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    try:
        return make_response({"goal" : goal.to_json()}, 200)
    except:
        abort(make_response({"details":f"goal {goal_id} not found"}, 404))


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    goal = validate_goal(goal_id)
    request_body = request.get_json()
    try: 
        goal.title = request_body["title"]
            
    except:
        abort(make_response(jsonify(f"goal {goal_id} not found"), 404))
    
    db.session.commit()

    return make_response({'goal':goal.to_json()}, 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_a_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({'details':f'Goal {goal.goal_id} "{goal.title}" successfully deleted'},200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks(goal_id):
    goal = Goal.query.get(goal_id)
    goal.tasks = []
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    for task_id in task_ids:
        task = Task.query.get(task_id)
        goal.tasks.append(task)

    # refer to the documentation and try
    # completing this endpoint yourself
    response_task_ids = []
    for task in goal.tasks:
        response_task_ids.append(task.task_id)
    
    db.session.commit()

    return {
            "id": goal.goal_id,
            "task_ids": response_task_ids
        }

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def tasks_of_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    tasks = []
    try:
        tasks = [task.make_json() for task in goal.tasks]

    except:
        abort(make_response(jsonify(f"goal not found"), 404))
    
    db.session.commit()    
    return {"id":goal.goal_id, "title":goal.title, "tasks" :tasks},200

    # refer to the documentation and try
    # completing this endpoint yourself

    
    db.session.commit()

    return {
            "id": goal.goal_id,
            "task_ids": response_task_ids
        }