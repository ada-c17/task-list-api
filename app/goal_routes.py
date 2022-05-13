from flask import Blueprint, jsonify, make_response, request
from requests import session
from app.helpers import validate_goal, validate_task
from app.models.goal import Goal
from app import db


goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

# Create goal


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {
            "details": "Invalid data"
        }, 400

    new_goal = Goal.create(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_json()}), 201)

# Get all goals


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    title_query = request.args.get("sort")

    if title_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif title_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()

    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_json())

    return jsonify(goals_response), 200

# Get one goal


@goal_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)
    return jsonify({"goal": goal.to_json()}), 200

# Update goal


@goal_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()

    goal.update(request_body)
    db.session.commit()

    return make_response(jsonify({"goal": goal.to_json()})), 200


# Delete goal
@goal_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)
    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {id} \"{goal.title}\" successfully deleted"}), 200)
