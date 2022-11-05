from app import db
from app.models.task import Task
from app.slack import SlackBot
from .routes_helper import success_msg, make_model_safely, replace_model_safely, get_model_by_id
from flask import Blueprint, jsonify, abort, make_response, request

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
slack_bot = SlackBot()

@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    new_task = make_model_safely(Task, request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201


@task_bp.route("", methods=["GET"])
def get_all_tasks():

    sort_title_query = request.args.get("sort")
    if sort_title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
        

    task_list = [task.to_dict() for task in tasks]

    return jsonify(task_list), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_model_by_id(Task, task_id)
    
    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    request_body = request.get_json()

    task = get_model_by_id(Task, task_id)
    replace_model_safely(task, request_body)

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_complete(task_id):
 
    task = get_model_by_id(Task, task_id)
    task.mark_completed()

    db.session.commit()

    slack_bot.send_notification(f"Someone just completed the task {task.title}")

    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(task_id):
    task = get_model_by_id(Task, task_id)

    task.mark_incompleted()

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_model_by_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return success_msg(f'Task {task.task_id} "{task.title}" successfully deleted', 200)

