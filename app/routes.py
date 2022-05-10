from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app import db


bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=("POST",))
def create_task():
    request_body = request.get_json()
    task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(task)
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 201)


@bp.route("/<task_id>", methods=("GET",))
def read_tasks(task_id):
    if not task_id:
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

    task = validate_task_id(task_id)
    return make_response(jsonify({"task": task.to_dict()}), 200)


@bp.route("/<task_id>", methods=("PUT",))
def update_task(task_id):
    request_body = request.get_json()
    task = validate_task_id(task_id)

    updated_task = task.override_task(request_body)
    db.session.add(updated_task)
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}, 200))


@bp.route("/<task_id>", methods=("DELETE",))
def delete_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()
    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": "Invalid data"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": "Task 1 not found"}, 404))
    return task