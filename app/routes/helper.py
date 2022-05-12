from flask import jsonify, abort, make_response
from app.models.task import Task

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify(f"task {task_id} invalid"), 400))
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify(f"task {task_id} not found"), 404))
    return task