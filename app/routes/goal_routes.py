from asyncio import Task
from flask import Blueprint
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import os
from .helper import validate_task, sort_filter_get


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@goal_bp.route("", methods=["POST"])
def create_goals():
    request_body = request.get_json()
    new_goal = Goal.create_goal(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal" : new_goal.to_json()}, 201)


@goal_bp.route("", methods=["GET"])
def read_all_goals():
    
    goals = sort_filter_get(Goal)
    
    goals_response = [goal.to_json() for goal in goals]    

    return make_response(jsonify(goals_response),200)



@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_task(Goal,goal_id)

    return make_response({"goal" : goal.to_json()}, 200)



@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    goal = validate_task(Goal,goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    
    db.session.commit()

    return make_response({'goal':goal.to_json()}, 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_a_goal(goal_id):
    goal = validate_task(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({'details':f'Goal {goal.goal_id} "{goal.title}" successfully deleted'},200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks(goal_id):
    goal = validate_task(Goal,goal_id)

    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    goal.tasks = [Task.query.get(task_id) for task_id in task_ids]

    response_task_ids = [task.task_id for task in goal.tasks]

    
    db.session.commit()

    return {
            "id": goal.goal_id,
            "task_ids": response_task_ids
        }

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def tasks_of_one_goal(goal_id):
    goal = validate_task(Goal,goal_id)

    tasks = [task.make_json() for task in goal.tasks]

    db.session.commit()  
    
    return {"id":goal.goal_id, "title":goal.title, "tasks" :tasks},200
