from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
import datetime
import requests
import os
#from sqlalchemy import asc, desc

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    order_by_query = request.args.get("sort")
    if order_by_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif order_by_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    return jsonify([task.to_dict() for task in tasks])


@tasks_bp.route("", methods=["POST"])
def post_task():
    request_body = request.get_json()

    if "title" in request_body and "description" in request_body:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
    else:
        abort(make_response({"details": "Invalid data"}, 400))


    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return jsonify({"task":task.to_dict()})


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    if "title" in request_body and "description" in request_body:
        task.title = request_body["title"]
        task.description = request_body["description"]
        if "completed_at" in request_body:
            task.completed_at = request_body["completed_at"]
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.commit()

    return make_response({"task":task.to_dict()})


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.completed_at = datetime.datetime.utcnow()
    db.session.commit()

    #Post message to slack
    PATH = "https://api.slack.com/api/chat.postMessage"
    SLACK_AUTH_TOKEN = os.environ.get("SLACK_TOKEN")

    query_params = {
        "channel":"task-list",
        "text":f'Someone just completed the task {task.title}'
    }
    header = {"Authorization":SLACK_AUTH_TOKEN}
    x = requests.post(PATH, params=query_params, headers=header)
    #end post

    return make_response({"task":task.to_dict()})


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.completed_at = None
    db.session.commit()

    return make_response({"task":task.to_dict()})













