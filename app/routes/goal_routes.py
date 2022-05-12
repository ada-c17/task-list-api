from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from sqlalchemy import desc


goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

def validate(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({'msg': f"Invalid id: '{id}'. ID must be an integer"}, 400))
    
    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message":f"goal {id} not found"}, 404))
    
    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(
            title=request_body["title"]
        )
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)
    
    db.session.add(new_goal)
    db.session.commit()
    response_body = {
        "goal": new_goal.return_goal_dict()
    }

    return make_response(jsonify(response_body), 201)

@goal_bp.route("", methods=["GET"])
def get_goals():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "desc":
            goals = Goal.query.order_by(desc(Goal.title))
        elif sort_query == "asc":
            goals = Goal.query.order_by(Goal.title)
    else:
        goals = Goal.query.all()
    response = []
    for goal in goals:
        response.append(goal.return_goal_dict())
    return jsonify(response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate(goal_id)
    response = {
        "goal": goal.return_goal_dict()
    }
    return jsonify(response)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response = {
        "goal": goal.return_goal_dict()
    }

    return make_response(jsonify(response), 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate(goal_id)
    db.session.delete(goal)
    db.session.commit()

    response = {'details': f'Goal {goal_id} "{goal.title}" successfully deleted'}

    return make_response(jsonify(response), 200)

