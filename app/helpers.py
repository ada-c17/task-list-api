from flask import abort, make_response, jsonify
from app.models.task import Task


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        return abort(make_response(jsonify(f"Task {task_id} is invalid"), 400))

    task = Task.query.get(task_id)

    if not task:
        return abort(make_response(jsonify(f"Task {task_id} does not exist"), 404))
    return task
