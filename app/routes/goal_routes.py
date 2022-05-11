from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from .helper import validate_task, validate_goal

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# CREATE goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.create(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))
        
    db.session.add(new_goal)
    db.session.commit()

    response_body = {}
    response_body['goal'] = new_goal.to_json()

    return make_response(jsonify(response_body), 201)


# GET ALL goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())

    return jsonify(goals_response), 200

# GET one goal
@goals_bp.route("/<goal_id>", methods=["GET"])  
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return jsonify({
        "goal": goal.to_json()
        })


# UPDATE one goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.commit()

    response_body = {}
    response_body['goal'] = goal.to_json()

    return make_response(jsonify(response_body), 200)

# DELETE one goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})), 200

# Create list of tasks of one goal
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_list_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    for id in request_body["task_ids"]:
        validate_task(id)
        task = Task.query.get(id)
        task.goal_id = goal.goal_id

    db.session.commit()

    response = {}
    response = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }
    return make_response(jsonify(response), 200)

# Get all tasks of one goal
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_of_one_goal(goal_id):

    goal = validate_goal(goal_id)
    tasks_response = []

    for task in goal.tasks:
        tasks_response.append(task.to_json())

    # response_body = goal.to_json()
    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
    }

    return make_response(jsonify(response_body), 200)
