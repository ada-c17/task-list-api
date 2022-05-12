from app import db
from app.models.goal import Goal
from app.models.task import Task 
from .routes_helpers import validate_id, validate_data, sort_records
from flask import Blueprint, request, jsonify

goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    if request.args.get("sort"):
        sort_query = request.args.get("sort")
        goals = sort_records(Goal, sort_query)
    else:
        goals = Goal.query.all() 

    goals_response = [goal.to_json() for goal in goals]
    return jsonify(goals_response), 200

@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_id(Goal, id)
    response_body = {}
    response_body["goal"] = goal.to_json()

    return jsonify(response_body), 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    new_goal = validate_data(Goal.create, request_body)

    db.session.add(new_goal)
    db.session.commit()

    response_body = {}
    response_body["goal"] = new_goal.to_json()

    return jsonify(response_body), 201

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_id(Goal, id)
    request_body = request.get_json()

    validate_data(goal.update, request_body)

    db.session.commit()
    
    response_body = {}
    response_body["goal"] = goal.to_json()
    
    return jsonify(response_body), 200

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_id(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({'details':f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200

@goals_bp.route("/<id>/tasks", methods=["POST"])
def post_existing_tasks_to_goal(id):
    goal = validate_id(Goal, id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        validate_id(Task, task_id)
        task = Task.query.get(task_id)
        task.goal_id = goal.id
    
    db.session.commit()
    
    response_body = {}
    response_body = {
            "id":goal.id,
            "task_ids": request_body["task_ids"]
            }
    
    return jsonify(response_body), 200

@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_all_tasks_by_goal(id):
    goal = validate_id(Goal, id)
    
    tasks_response = [task.to_json() for task in goal.tasks]
    
    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }

    return jsonify(response_body), 200