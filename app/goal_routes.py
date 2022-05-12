
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from app import db


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def error_message(message, status_code):
        abort(make_response(jsonify(dict(details=message)), status_code))

def make_goal_safely(data_dict):
    try:
        return Goal.from_dict(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)

def replace_goal_safely(goal, data_dict):
    try:
        goal.replace_details(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)

def get_goal_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)

    goal = Goal.query.get(id)
    if goal:
        return goal
    
    error_message(f"No goal with id {id} found", 404)

# POST /goals
@goals_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = make_goal_safely(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

# GET /goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    sort_param = request.args.get("sort")

    if sort_param == 'asc':
        goals = Goal.query.order_by(Goal.title.asc())
    elif sort_param == 'desc':
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    
    result_list = [goal.to_dict() for goal in goals]

    return jsonify(result_list)

# GET /goals/<goal_id>
@goals_bp.route("/<goal_id>", methods=["Get"])
def read_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)
    return jsonify({"goal":goal.to_dict()})

# PUT /goals/<goal_id>
@goals_bp.route("/<goal_id>", methods=["PUT"])
def replace_goal_by_id(goal_id):
    request_body = request.get_json()
    goal = get_goal_record_by_id(goal_id)

    replace_goal_safely(goal, request_body)

    db.session.add(goal)
    db.session.commit()

    return jsonify({"goal":goal.to_dict()})

# DELETE /goals/<goal_id>
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})
