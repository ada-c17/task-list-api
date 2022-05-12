from app import db
from app.models.task import Task
from app.routes.utils.slack_bot import SlackClient
from app.routes.utils.helper import get_or_abort, get_JSON_request_body
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    title_query = request.args.get("sort")
    if title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    else:
        tasks = Task.query

    tasks_response = [task.to_JSON_response()["task"] for task in tasks]

    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):

    task = get_or_abort(Task, task_id)

    return jsonify(task.to_JSON_response()), 200


@tasks_bp.route("", methods=["POST"])
def create_task():

    new_task = Task.from_JSON_request()

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_JSON_response()), 201


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = get_or_abort(Task, task_id)

    task.update_from_JSON_request()

    db.session.commit()

    return jsonify(task.to_JSON_response()), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_as_complete(task_id):

    task = get_or_abort(Task, task_id)

    task.completed_at = datetime.utcnow()

    db.session.commit()

    slack_client = SlackClient()
    notification_text = f"Someone just completed the task {task.title}"
    slack_client.send_notification(notification_text)

    return jsonify(task.to_JSON_response()), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_as_incomplete(task_id):

    task = get_or_abort(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return jsonify(task.to_JSON_response()), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    task = get_or_abort(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200
