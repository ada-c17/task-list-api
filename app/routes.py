
from sqlalchemy import desc
from app import db
from app.models.task import Task
from app.helper import validate_task
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

# POST
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body.keys():
        return {"details": "Invalid data"}, 400
    elif "description" not in request_body.keys():
        return {"details": "Invalid data"}, 400
    else:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])

        db.session.add(new_task)
        db.session.commit()

        return { "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }}, 201


# GET all
@tasks_bp.route("", methods=["GET"])
def read_task():

    sort_query = request.args.get("sort")
    if sort_query == 'asc':
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query == 'desc':
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
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

# GET one Task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)

    return { "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
    }}, 200

# UPDATE one Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    
    return { "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
    }}, 200

# DELETE one Task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200
