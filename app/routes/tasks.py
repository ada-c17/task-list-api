from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from app import db
from datetime import datetime
from app.routes.helpers import valid_task, display_task, post_slack_message, check_completed_at

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        task = Task(
                title = request_body["title"],
                description = request_body["description"],
                # if user does not input completed_at, will return None
                # if user does include completed_at but not in the correct format, return 400 and abort
                # accept completed_at datetime format string: 'Thu, 12 May 2022 04:19:18 GMT'
                completed_at = check_completed_at(request_body)
                )
    except KeyError:
        abort(make_response({"details":"Invalid data"}, 400))  

    db.session.add(task)
    db.session.commit()

    return make_response(
        jsonify({"task":display_task(task)}), 201
    )

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    param = request.args.get("sort")
    if param:
        is_desc = True if param == "desc" else False
        tasks.sort(reverse=is_desc, key=lambda task:task.title)         
            
    res = []
    for task in tasks:
        res.append(display_task(task))

    return make_response(jsonify(res), 200)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = valid_task(task_id)
    res = display_task(task)
    if task.goal_id:
        res["goal_id"] = task.goal_id 

    return make_response(
        jsonify({"task":res}), 200
    )
   
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = valid_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = check_completed_at(request_body)
    db.session.commit()

    return make_response(
        jsonify({"task":display_task(task)}), 200
    )

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def remove_task(task_id):
    task = valid_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response(
        jsonify(details=f"Task {task.task_id} \"{task.title}\" successfully deleted"), 200
    )

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = valid_task(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    post_slack_message(f"Someone just completed the task {task.title}")

    return make_response(
        jsonify({"task":display_task(task)}), 200
    )

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = valid_task(task_id)
    if task.completed_at:
        task.completed_at = None
        db.session.commit()

    return make_response(
        jsonify({"task":display_task(task)}), 200
    )