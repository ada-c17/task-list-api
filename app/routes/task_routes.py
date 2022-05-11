from urllib import response
from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task
from sqlalchemy import desc
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_OAUTH_TOKEN = os.environ.get("SLACK_OAUTH_TOKEN")

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

def validate_task(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({'msg': f"Invalid id: '{id}'. ID must be an integer"}, 400))
    
    task = Task.query.get(id)

    if not task:
        abort(make_response({"message":f"task {id} not found"}, 404))
    
    return task


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
        )
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]
    
    db.session.add(new_task)
    db.session.commit()
    response_body = {
        "task": new_task.return_task_dict()
    }

    return make_response(jsonify(response_body), 201)

@task_bp.route("", methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "desc":
            tasks = Task.query.order_by(desc(Task.title))
        elif sort_query == "asc":
            tasks = Task.query.order_by(Task.title)
    else:
        tasks = Task.query.all()
    response = []
    for task in tasks:
        response.append(task.return_task_dict())
    return jsonify(response)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    response = {
        "task": task.return_task_dict()
    }
    return jsonify(response)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {
        "task": task.return_task_dict()
    }

    return make_response(jsonify(response), 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    response = {'details': f'Task {task_id} "{task.title}" successfully deleted'}

    return make_response(jsonify(response), 200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.datetime.now()
    db.session.commit()

    message = "Someone just completed the task " + task.title

    path = "https://slack.com/api/chat.postMessage"
    headers = {'Authorization': f'Bearer {SLACK_OAUTH_TOKEN}'}
    params = {"channel": "task-notifications", "text": message}

    requests.post(path,data=params,headers=headers)
    

    response = {"task": task.return_task_dict()}

    return make_response(jsonify(response), 200)

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    response = {"task": task.return_task_dict()}

    return make_response(jsonify(response), 200)