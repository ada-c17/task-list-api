from flask import jsonify, abort, make_response
from app.models.task import Task

def validate_task(cls,task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response(jsonify(f"task {task_id} invalid"), 400))
    obj = cls.query.get(task_id)

    if not obj:
        abort(make_response(jsonify(f"task {task_id} not found"), 404))
    return obj