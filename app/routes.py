from flask import Blueprint, make_response, request,jsonify, abort
from app import db
from app.models.task import Task


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return jsonify({"task":
    {"id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": task.completed_at}
    }) 
    #if this task doesn't exist, it should automatically return empty []


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    print(request_body)
    new_task = Task(title = request_body["title"],
                    description = request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response_body = {"task":
        {"id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at}
    }

    if response_body["task"]["is_complete"] == None:
        response_body["task"]["is_complete"] = False
    return jsonify(response_body), 201

