from urllib import response
from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task

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

    db.session.add(new_task)
    db.session.commit()
    response_body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }

    return make_response(jsonify(response_body), 201)

@task_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    response = []
    for task in tasks:
        response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    return jsonify(response)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
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
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
            }
    }

    return make_response(jsonify(response), 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    response = {'details': f'Task {task_id} "{task.title}" successfully deleted'}

    return make_response(jsonify(response), 200)
