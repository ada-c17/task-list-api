from flask import Blueprint, jsonify, abort, make_response, request
from .models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#GET ALL TASKS
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

	title_query = request.args.get("title")
	description_query = request.args.get("description")
	completed_at_query = request.args.get("completed_at")

	if title_query:
		tasks = Task.query.filter_by(length_of_year=title_query)
	elif description_query:
		tasks = Task.query.filter_by(description=description_query)
	elif completed_at_query:
		tasks = Task.query.filter_by(circumference=completed_at_query)
	else:
		tasks = Task.query.all()

	tasks_response = []

	for task in tasks:
		tasks_response.append(task.to_json())

	return jsonify(tasks_response)
