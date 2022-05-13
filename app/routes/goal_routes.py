from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app.routes.helper import get_or_abort

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# Validate there is title when creating or updating a goal
def validate_create_or_put():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        rsp = {
            "details": "Invalid data"
        }
        abort(make_response(jsonify(rsp), 400))
    
    return new_goal


@goals_bp.route('', methods=['POST'])
def create_one_goal():
    new_goal = validate_create_or_put()
    
    db.session.add(new_goal)
    db.session.commit()
    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route('', methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    rsp = []
    
    for goal in goals:
        rsp.append(goal.to_dict())

    return jsonify(rsp), 200

@goals_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    chosen_goal = get_or_abort(Goal, goal_id)

    rsp = {"goal": chosen_goal.to_dict()}
    return jsonify(rsp), 200

@goals_bp.route("/<goal_id>", methods=['PUT'])
def put_one_goal(goal_id):
    chosen_goal = get_or_abort(Goal, goal_id)
    new_goal = validate_create_or_put()

    chosen_goal.title = new_goal.title
    
    db.session.commit()    
    
    rsp = {"goal": chosen_goal.to_dict()}
    return jsonify(rsp), 200

@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_one_goal(goal_id):
    chosen_goal = get_or_abort(Goal, goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()
    rsp = {
        "details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'
    }
    return jsonify(rsp), 200


@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def post_task_ids_to_goal(goal_id):
    chosen_goal = get_or_abort(Goal, goal_id)
    request_body = request.get_json()
    
    for task_id in request_body["task_ids"]:
        task = get_or_abort(Task, task_id)
        task.goal_id = goal_id
    
    # Question
    # assigning value to rsp{"task_ids"}
    # or can I just do request_body["task_ids"]?
    task_ids = []
    for task in chosen_goal.tasks:
        task_ids.append(task.task_id)

    db.session.commit()
    rsp = {
        "id": chosen_goal.goal_id,
        "task_ids": task_ids 
    }
    return jsonify(rsp), 200

@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_task_ids_to_goal(goal_id):
    chosen_goal = get_or_abort(Goal, goal_id)
    
    goal_dict = chosen_goal.to_dict()
    goal_dict["tasks"] = [] # can i remove these ["tasks"]? refactor
    
    for task in chosen_goal.tasks:
        goal_dict["tasks"].append(task.to_dict())

    db.session.commit()

    return jsonify(goal_dict), 200