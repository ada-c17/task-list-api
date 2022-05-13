from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app import db
import datetime
import os
from app.slack_helper import *

SLACK_OAUTH_TOKEN = os.environ.get("SLACK_OAUTH_TOKEN")

tasks_bp = Blueprint("tasks",__name__,url_prefix="/tasks")

@tasks_bp.route("",methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    query_params = request.args
    if query_params.get("title"):
        tasks = Task.query.filter_by(title=query_params.get("title"))
    # default sort is by title in an ascending order
    if query_params.get("sort"):
        task_attribute = Task.task_id if query_params.get("sort_by") == "title" else Task.title
        if query_params.get("sort") == "desc":
            tasks = Task.query.order_by(task_attribute.desc())
        else:
            tasks = Task.query.order_by(task_attribute)
    response = []
    if tasks:
        for task in tasks:
            response.append(task.to_json(task=False))
    return make_response(jsonify(response),200)

@tasks_bp.route("",methods=["POST"])
def make_task():
    request_body = request.get_json()
    new_task = Task.from_json(request_body)
    db.session.add(new_task)
    db.session.commit()
    response = new_task.to_json()
    return make_response(response,201)

@tasks_bp.route("/<id>",methods=["GET"])
def get_task(id):
    task = Task.validate_id(id)
    response = task.to_json()
    return make_response(response,200)

@tasks_bp.route("/<id>",methods=["PATCH","PUT"])
def update_task(id):
    task = Task.validate_id(id)
    request_body = request.get_json()
    if request.method=="PATCH":
        if request_body.get("title"):
            task.title = request_body["title"]
        if request_body.get("description"):
            task.description = request_body["description"]
    else:
        try:
            task.title = request_body["title"]
            task.description = request_body["description"]
        except KeyError:
            return make_response({"details":"Incomplete data"},400)
    db.session.commit()
    response = task.to_json()
    return make_response(response,200)

@tasks_bp.route("/<id>",methods=["DELETE"])
def delete_task(id):
    task = Task.validate_id(id)
    db.session.delete(task)
    db.session.commit()
    return make_response({"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"},200)

@tasks_bp.route("/<id>/mark_complete",methods=["PATCH"])
def complete_task(id):
    task = Task.validate_id(id)
    task.completed_at = datetime.datetime.utcnow()
    db.session.commit()
    post_slack_msg(task)
    response = task.to_json()
    return make_response(response,200)

@tasks_bp.route("/<id>/mark_incomplete",methods=["PATCH"])
def uncomplete_task(id):
    task = Task.validate_id(id)
    task.completed_at = None
    db.session.commit()
    response = task.to_json()
    return make_response(response,200)