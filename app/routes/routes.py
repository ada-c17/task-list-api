from urllib import response
from app import db
from app.models.task import Task
from flask import Blueprint, make_response, request, jsonify, abort
from .helpers import validate_task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Get all tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(task.to_json())
    
    return jsonify(tasks_response),200

# Get one task
@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    # tasks_response = []
    task = validate_task(id)

    return jsonify({"task":task.to_json()}),200

# Create task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try: 
        new_task = Task.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"},400)
    
    db.session.add(new_task)
    db.session.commit()

    
    return jsonify({"task":new_task.to_json()}), 201
    
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json()
    task.update(request_body)
    db.session.commit()

    return jsonify({"task":task.to_json()}), 200

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"details": f'Task {id} "{task.to_json()["title"]}" successfully deleted'}), 200
