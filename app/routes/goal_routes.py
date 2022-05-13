from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, request
from app.models.task import Task
from app.routes.helper import validate_id, validate_goal_attributes

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route('', methods=['POST'])
def create_one_goal():
    new_goal = validate_goal_attributes(request.get_json())
    
    db.session.add(new_goal)
    db.session.commit()
    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route('', methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    rsp = [goal.to_dict() for goal in goals]

    return jsonify(rsp), 200

@goals_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    chosen_goal = validate_id(Goal, goal_id)

    rsp = {"goal": chosen_goal.to_dict()}
    return jsonify(rsp), 200

@goals_bp.route("/<goal_id>", methods=['PUT'])
def put_one_goal(goal_id):
    chosen_goal = validate_id(Goal, goal_id)
    new_goal = validate_goal_attributes(request.get_json())

    chosen_goal.title = new_goal.title
    
    db.session.commit()    
    
    rsp = {"goal": chosen_goal.to_dict()}
    return jsonify(rsp), 200

@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_one_goal(goal_id):
    chosen_goal = validate_id(Goal, goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()
    rsp = {
        "details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'
    }
    return jsonify(rsp), 200


@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def post_task_ids_to_goal(goal_id):
    chosen_goal = validate_id(Goal, goal_id)
    request_body = request.get_json()
    
    for task_id in request_body["task_ids"]:
        task = validate_id(Task, task_id) #question, necessary to validate?
    #   task = validate_attributes(Task) #question, necessary to validate?
        task.goal_id = goal_id
    
    # Question
    # assigning value to rsp{"task_ids"}
    # or can I just do request_body["task_ids"]?
    task_ids = [task.task_id for task in chosen_goal.tasks]

    db.session.commit()
    rsp = {
        "id": chosen_goal.goal_id,
        "task_ids": task_ids 
    }
    return jsonify(rsp), 200

@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_task_ids_to_goal(goal_id):
    chosen_goal = validate_id(Goal, goal_id)
    
    goal_dict = chosen_goal.to_dict()
    # can i remove these ["tasks"]? refactor    
    goal_dict["tasks"] = [task.to_dict() for task in chosen_goal.tasks]

    db.session.commit()

    return jsonify(goal_dict), 200