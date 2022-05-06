from asyncio import tasks
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from .models.helpers import validate_task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#GET ALL TASKS
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

	title_query = request.args.get("title")
	description_query = request.args.get("description")
	is_complete_query = request.args.get("completed_at")

	if title_query:
		tasks = Task.query.filter_by(length_of_year=title_query)
	elif description_query:
		tasks = Task.query.filter_by(description=description_query)
	elif is_complete_query:
		tasks = Task.query.filter_by(completed_at=is_complete_query)
	else:
		tasks = Task.query.all()

	tasks_response = []

	for task in tasks:
		tasks_response.append(task.to_json())

	return jsonify(tasks_response)

# GET ONE TASK


@tasks_bp.route("/<id>", methods=["GET"])
def get_one_tasks(id):
    task = validate_task(id)
    print(task)
    return jsonify({"task": task.to_json()}), 200

# CREATE PLANET


@tasks_bp.route("", methods=["POST"])
def create_task():
	request_body = request.get_json()

	new_task = Task.create(request_body)

	db.session.add(new_task)
	db.session.commit()

	return jsonify({"task": new_task.to_json()}), 201

#PUT one task
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)

    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return jsonify({"task": task.to_json()}), 200

#DELETE ONE PLANET


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {id} "{task.title}" successfully deleted'}), 200
