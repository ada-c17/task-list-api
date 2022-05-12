from flask import Blueprint, jsonify, request
from app.models.goal import Goal
from app.models.task import Task
from app import db
from ..models.helpers import validate_object

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods = ["GET"])
def get_all_goals():
	title_query = request.args.get("title")

	goals = Goal.query.filter_by(length_of_year=title_query) if title_query else Goal.query.all()

	goals_response = [goal.to_json() for goal in goals]

	return jsonify(goals_response), 200

@goals_bp.route("/<id>", methods=["GET"])
def get_one_goals(id):
    goal = validate_object(Goal, id)

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
    goal = validate_object(Goal, id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": goal.to_json()}), 200

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_one_goal(id):
    goal = validate_object(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {id} "{goal.title}" successfully deleted'}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_id_to_goal(goal_id):
	goal = validate_object(Goal, goal_id)

	request_body = request.get_json()

	for task_id in request_body["task_ids"]:
		task = validate_object(Task, task_id)
		goal.tasks.append(task) 

	db.session.commit()

	return jsonify({"id": goal.goal_id, "task_ids": request_body["task_ids"]}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks(goal_id):
	goal = validate_object(Goal, goal_id)

	response_body = goal.to_json()

	response_body["tasks"] = [task.to_json() for task in goal.tasks]

	return jsonify(response_body), 200
