from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    response_body = []

    for task in tasks: # make dict then append response_body list
        response = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
        }
        if task.completed_at:
            response["is_complete"] = True
        else:
            response["is_complete"] = False
        response_body.append(response)
        
    print(response_body)

    return jsonify(response_body), 200