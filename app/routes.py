from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app import db


bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=("POST",))
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": Task.to_dict(new_task)}, 201)


@bp.route("/<task_id>", methods=("GET",))
def read_tasks(task_id):
    if not task_id:
        tasks = Task.query.all()
        return jsonify([Task.to_dict(task) for task in tasks])

    task = validate_task_id(task_id)
    return make_response(jsonify({"task": Task.to_dict(task)}, 200))


@bp.route("/<task_id>", methods=("PUT",))
def update_task(task_id):
    request_body = request.get_json()
    task = validate_task_id(task_id)

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return make_response(jsonify({"task": Task.to_dict(task)}, 200))


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
        abort(make_response({"message": "Invalid task id"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": "Task id not found"}, 404))
    return task