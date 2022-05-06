from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return jsonify(
        {
            "details": "Invalid data"
        }), 400
    else:
        new_task = Task(title=request_body["title"],description = request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    is_complete = check_if_task_complete(new_task)

    response_body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
        }
    }
    return make_response(jsonify(response_body), 201)

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify({"details": "Invalid data"}, 400)))

    task = Task.query.get(task_id)
    if task:
        return task

    abort(make_response({"details": "Item not found"}, 404))

def check_if_task_complete(new_task):
    if new_task.completed_at:
        is_complete = True
    else:
        is_complete = False
        return is_complete

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args
    if "title" in params:
        task_title = params["title"]
        tasks = Task.query.filter_by(title = task_title)
    else: tasks = Task.query.all()

    response = []

    for task in tasks:
        response.append(
            {"id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": check_if_task_complete(task)
            }
        )
    return jsonify(response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": check_if_task_complete(task)
        }
    }),200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify(
        {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": check_if_task_complete(task)
            }
        }
    ), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200