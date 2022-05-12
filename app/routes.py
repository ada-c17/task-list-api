from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task(title = request_body["title"], description = request_body["description"])
        db.session.add(new_task)
        db.session.commit()
    except:
        abort(make_response(jsonify({"message":f"invalid input"}), 400))
    return make_response(jsonify({"task": new_task.to_json()}), 201)

@task_bp.route("", methods=["GET"])
def fetch_all_tasks():

    # title_query = request.args.get("title")
    # if title_query:
    #     tasks = Task.query.filter_by(title_query)
    # else:
    tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(task.to_json())
    return make_response(jsonify(task_response),200)