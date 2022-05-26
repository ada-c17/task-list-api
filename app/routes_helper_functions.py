from flask import jsonify, abort, make_response
from .models.task import Task

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        error_message(f"task {task_id} invalid", 400)

    task = Task.query.get(task_id)

    if not task:
        error_message(f"task {task_id} not found", 404)

    return task
