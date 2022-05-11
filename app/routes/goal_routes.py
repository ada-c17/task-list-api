from flask import Blueprint, jsonify, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from ..models.helpers import post_slack_message, validate_task, validate_goal

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods = ["GET"])
def get_all_goals():

	title_query = request.args.get("title")
	# figure out getattr()

	if title_query:
		goals = Goal.query.filter_by(length_of_year=title_query)
	else:
		goals = Goal.query.all()

	goals_response = []

	for goal in goals:
		goals_response.append(goal.to_json())

	return jsonify(goals_response), 200


@goals_bp.route("/<id>", methods=["GET"])
def get_one_goals(id):
    goal = validate_goal(id)
    print(goal)
    return jsonify({"goal": goal.to_json()}), 200


@goals_bp.route("", methods=["POST"])
def create_goal():
	request_body = request.get_json()

	new_goal = Goal.create(request_body)

	db.session.add(new_goal)
	db.session.commit()

	return jsonify({"goal": new_goal.to_json()}), 201


@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)

    request_body = request.get_json()

    goal.update(request_body)

    db.session.commit()

    return jsonify({"goal": goal.to_json()}), 200


@goals_bp.route("/<id>", methods=["DELETE"])
def delete_one_goal(id):
    goal = validate_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {id} "{goal.title}" successfully deleted'}), 200
