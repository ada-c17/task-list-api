from sqlalchemy import asc, desc
from app import db
from app.models.task import Task 
from app.models.goal import Goal 
from .task_routes import validate_task
from flask import Blueprint, abort, jsonify, make_response, request
import datetime
from sqlalchemy.sql.functions import now 
import requests

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


##### Goal Model #####
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return {
        "details": "Invalid data"
    }, 400
        
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title,
            }
            }), 201


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
        })
    return jsonify(goals_response)


# helper function:
def validate_goal(id_of_goal):
    try:
        id_of_goal = int(id_of_goal)
    except:
        abort(make_response({"message":f"goal {id_of_goal} invalid"}, 400))

    goal = Goal.query.get(id_of_goal)

    if not goal:
        abort(make_response({"message":f"goal {id_of_goal} not found"}, 404))

    return goal


@goals_bp.route("/<id_of_goal>", methods=["GET"])
def read_one_goal(id_of_goal):
    goal = validate_goal(id_of_goal)
    return jsonify({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
            }
            })


@goals_bp.route("/<id_of_goal>", methods=["PUT"])
def replace_goal(id_of_goal):
    goal = validate_goal(id_of_goal)
    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()

    return jsonify({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
            }
            })


@goals_bp.route("/<id_of_goal>", methods=["DELETE"])
def delete_task(id_of_goal):
    goal = validate_goal(id_of_goal)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal 1 "{goal.title}" successfully deleted'
    }


@goals_bp.route("/<id_of_goal>/tasks", methods=["POST"])
def create_tasks_from_goal(id_of_goal):
    goal = validate_goal(id_of_goal)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = validate_task(task_id)
        goal.tasks.append(task)

    db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }


@goals_bp.route("/<id_of_goal>/tasks", methods=["GET"])
def read_tasks_from_goal(id_of_goal):
    goal = validate_goal(id_of_goal)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append({
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            })
        
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
    })