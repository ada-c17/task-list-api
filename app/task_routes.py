from urllib import response
from flask import Blueprint, make_response,jsonify, request
import requests
from app import db
from app.models.task import Task
from .helper_functions import get_task_record_by_id, update_task_safely
from datetime import datetime  
import os
from dotenv import load_dotenv
load_dotenv()

SLACK_AUTH = os.environ.get("SLACK_AUTH")
SLACK_PATH = "https://slack.com/api/chat.postMessage"

tasks_bp = Blueprint("Tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET",])
def get_tasks():
    sort_param = request.args.get("sort")
    if sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc()) 
    else:
        tasks = Task.query.all()
    response = [task.self_to_dict() for task in tasks]
    return make_response(jsonify(response))

@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = get_task_record_by_id(id)
    response = task.self_to_dict()
    if task.goal_id:
        response["goal_id"]=task.goal_id
    return jsonify(task=response)

@tasks_bp.route("", methods=["POST",])
def add_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"]
                    )
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
    except KeyError:
        return make_response(jsonify(details="Invalid data"),400)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(task=new_task.self_to_dict()),201)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = get_task_record_by_id(id)

    request_body = request.get_json()

    update_task_safely(task, request_body)

    db.session.commit()

    return make_response(jsonify(task=task.self_to_dict()))

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def update_task_complete(id):
    task = get_task_record_by_id(id)
    task.completed_at = datetime.now()
    db.session.commit()

    header_params = {"Authorization": SLACK_AUTH}
    query_params = {
        "channel": "test-channel",
        "text": f"Task marked complete: {task.title}"}
    requests.post(SLACK_PATH, params=query_params, headers=header_params)

    return make_response(jsonify(task=task.self_to_dict()))

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(id):
    task = get_task_record_by_id(id)
    task.completed_at = None
    db.session.commit()

    header_params = {"Authorization": SLACK_AUTH}
    query_params = {
        "channel": "test-channel",
        "text": f"Task marked incomplete: {task.title}"}
    requests.post(SLACK_PATH, params=query_params, headers=header_params)

    return make_response(jsonify(task=task.self_to_dict()))

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = get_task_record_by_id(id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify(details=f"Task {task.task_id} \"{task.title}\" successfully deleted"),200)
