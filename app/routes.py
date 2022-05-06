from flask import Blueprint
from os import abort
from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    )
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }, 201 

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_book(task_id):
    try: 
        task_id = int(task_id)
    except ValueError:
        response = {
            "message" : f"Invalid id: {task_id}"}
        return jsonify(response), 400
    one_task = Task.query.get(task_id)

    if one_task is None:
        response = {"message": f" Could not find a planet with id {task_id}"}
        return jsonify(response), 404
    
    response = { "task": {
                "id" : one_task.task_id,
                "title": one_task.title,
                "description": one_task.description,
                "is_complete": False
                }
            }
    return jsonify(response), 200