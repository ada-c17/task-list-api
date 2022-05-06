import json
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods = ["POST"])
def manage_post_tasks():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(new_task.to_dictionary()), 201)

@tasks_bp.route("", methods=["GET"])
def manage_get_tasks():
    tasks = Task.query.all()
    title_query = request.args.get("title")

    if title_query:
        tasks = Task.query.filer_by(title=title_query)
    else:
        tasks = Task.query.filter_by(title=title_query)

    tasks_response = [task.to_dictionary() for task in tasks]

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = validate_task(task_id)

    return jsonify(task.to_dictionary())


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))