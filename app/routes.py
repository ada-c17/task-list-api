from app import db
from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({"msg":f"Invalid task id: {task_id}. ID must be an integer."}), 400


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"], 
                        description=request_body["description"])
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": {"id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": False,}}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_sort_query = request.args.get("sort")
    if title_sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        response.append(
            {"id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False}
        )

    return jsonify(response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    requested_task = Task.query.get(task_id)

    if requested_task is None:
        return jsonify({"msg":f"Could not find task with id: {task_id}"}), 404
    
    return {"task": {"id": requested_task.task_id,
                    "title": requested_task.title,
                    "description": requested_task.description,
                    "is_complete": False}}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    requested_task = Task.query.get(task_id)
    if requested_task is None:
        return jsonify({"msg":f"Could not find task with id: {task_id}"}), 404

    requested_task.title = request_body["title"]
    requested_task.description = request_body["description"]

    db.session.commit()

    return {"task": {"id": requested_task.task_id,
                    "title": requested_task.title,
                    "description": requested_task.description,
                    "is_complete": False}}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    requested_task = Task.query.get(task_id)
    if requested_task is None:
        return jsonify({"msg":f"Could not find task with id: {task_id}"}), 404

    db.session.delete(requested_task)
    db.session.commit()

    return jsonify({"details": f'Task {requested_task.task_id} "{requested_task.title}" successfully deleted'})

