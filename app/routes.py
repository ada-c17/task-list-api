from wsgiref.util import request_uri
from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app import db
import datetime
import os

tasks_bp = Blueprint("tasks",__name__,url_prefix="/tasks")

@tasks_bp.route("",methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query.lower() == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        if sort_query.lower() == "asc":
            tasks = Task.query.order_by(Task.title)
    else:
        tasks = Task.query.all()
    response = []
    if tasks:
        for task in tasks:
            response.append({
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete":False if not task.completed_at else True
            })
    return make_response(jsonify(response),200)

@tasks_bp.route("",methods=["POST"])
def make_task():
    request_body = request.get_json()
    completed_at = request_body.get("completed_at",None)
    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=completed_at
        )
    except KeyError:
        return make_response({"details":"Invalid data"},400)
    db.session.add(new_task)
    db.session.commit()
    response = {
        "task": {
            "id":new_task.task_id,
            "title":new_task.title,
            "description":new_task.description,
            "is_complete":False if not new_task.completed_at else True
        }
    }
    return make_response(response,201)

@tasks_bp.route("/<id>",methods=["GET"])
def get_task(id):
    try:
        id = int(id)
    except ValueError:
        return make_response({"details":"Invalid data"},400)
    task = Task.query.get(id)
    if not task:
        return make_response({"details":f"Task #{id} does not exist"}, 404)
    response = {
        "task": {
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete":False if not task.completed_at else True
        }
    }
    return make_response(response,200)

@tasks_bp.route("/<id>",methods=["PATCH","PUT"])
def update_task(id):
    try:
        id = int(id)
    except ValueError:
        return make_response({"details":"Invalid data"},400)
    task = Task.query.get(id)
    if not task:
        return make_response({"details":f"Task #{id} does not exist"}, 404)
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
    response = {
        "task": {
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete":False if not task.completed_at else True
        }
    }
    return make_response(response,200)

@tasks_bp.route("/<id>",methods=["DELETE"])
def delete_task(id):
    try:
        id = int(id)
    except ValueError:
        return make_response({"details":"Invalid data"},400)
    task = Task.query.get(id)
    if not task:
        return make_response({"details":f"Task #{id} does not exist"}, 404)
    db.session.delete(task)
    db.session.commit()
    return make_response({"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"},200)

@tasks_bp.route("/<id>/mark_complete",methods=["PATCH"])
def complete_task(id):
    try:
        id = int(id)
    except ValueError:
        return make_response({"details":"Invalid data"},400)
    task = Task.query.get(id)
    if not task:
        return make_response({"details":f"Task #{id} does not exist"}, 404)
    task.completed_at = datetime.datetime.utcnow()
    db.session.commit()
    response = {
        "task": {
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete":False if not task.completed_at else True
        }
    }
    return make_response(response,200)

@tasks_bp.route("/<id>/mark_incomplete",methods=["PATCH"])
def uncomplete_task(id):
    try:
        id = int(id)
    except ValueError:
        return make_response({"details":"Invalid data"},400)
    task = Task.query.get(id)
    if not task:
        return make_response({"details":f"Task #{id} does not exist"}, 404)
    task.completed_at = None
    db.session.commit()
    response = {
        "task": {
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete":False if not task.completed_at else True
        }
    }
    return make_response(response,200)