from datetime import datetime
from email import message
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from sqlalchemy import asc, desc
from app.models.goal import Goal
from app.models.task import Task

goal_bp = Blueprint('goals', __name__, url_prefix='/goals')

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response(jsonify({'details': 'Invalid data'}), 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        return abort(make_response(jsonify(f"Goal {goal_id} not found"), 404))
    
    return goal


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        new_goal = Goal(
            title = request_body["title"]
        )

        db.session.add(new_goal)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query
    goals = goals.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    
    return {"goal": goal.to_dict()}

@goal_bp.route("/<goal_id>", methods=["PUT"])
def replace_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return {"goal": goal.to_dict()}

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({'details': f'Goal "{goal.title}" successfully deleted'})

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):

    goal = validate_goal(goal_id)

    tasks_response = []
    for task in goal.tasks:
        is_complete = bool(task.completed_at)
        tasks_response.append(
            {
            "id": task.task_id,
            "goal_id": goal.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete
            }
        )
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response})

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_to_goal(goal_id):
    tasks_response = []
    request_body = request.get_json()
    
    search_key = 'task'
    key_name = ([key for key in request_body.keys() if search_key in key])
    task_ids = ([val for key, val in request_body.items() if search_key in key])
    goal = validate_goal(goal_id)

    for i in range(len(task_ids[0])):
        task_id = task_ids[0][i]

        task = Task.query.get(int(task_id))
        
        goal.tasks.append(task)
        db.session.commit()

        tasks_response.append(
                task_id
            )

    ret_key = key_name[0]

    return make_response(jsonify({
        "id": goal.goal_id,
        ret_key: tasks_response
    }), 200)