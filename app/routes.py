from xmlrpc.client import boolean
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"], 
        description=request_body["description"]
        )

    db.session.add(new_task)
    db.session.commit()
    db.session.expire(new_task)
    
    return make_response(new_task.to_dict(), 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    return jsonify(tasks_response)