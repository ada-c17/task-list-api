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
