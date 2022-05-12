import slack
from pathlib import Path
from dotenv import load_dotenv
from app.models.task import Task
from app import db
import os
import datetime

from ..helpers import validate_object
from ..helpers import validate_new_data
# from ..helpers import validate_task
from flask import Blueprint, request, jsonify, make_response, abort

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.create(request_body)
        db.session.add(new_task)
        db.session.commit()
    except KeyError:
        return abort(make_response(jsonify({"details": "Invalid data"}), 400))
    return new_task.to_json(), 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = [task.to_json()["task"] for task in tasks]

    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_object(Task, task_id)

    if task.goal_id:
        task.to_json()["task"]["goal_id"] = task.goal_id

    return jsonify(task.to_json()), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_object(Task, task_id)
    request_body = request.get_json()

    task.update(request_body)
    db.session.commit()
    return jsonify(task.to_json()), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_object(Task, task_id)

    db.session.delete(task)
    db.session.commit()
    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_update(task_id):
    task = validate_object(Task, task_id)
    request_body = request.get_json()

    if task.completed_at == None:
        task.completed_at = datetime.datetime.now()

    db.session.commit()
    client.chat_postMessage(channel='#task-notifications',
                            text=f"task: '{task.title}' is complete")
    return task.to_json(), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_update(task_id):
    task = validate_object(Task, task_id)
    request_body = request.get_json()

    if task.completed_at != None:
        task.completed_at = None

    db.session.commit()
    return task.to_json(), 200
