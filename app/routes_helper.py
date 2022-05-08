from flask import abort, make_response, jsonify
from app.models.task import Task

def check_task_exists(task_id):
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify({"error": f"Task {task_id} does not exist"}), 404))
    
    return task

def try_to_make_task(response_body):
    try:
        return Task.make_task(response_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
