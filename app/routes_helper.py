from app.models.task import Task
from flask import jsonify, make_response, abort

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify(dict(details=f"Invalid task id: {task_id}")), 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify(dict(details=f"Task not found")), 404))
    else:
        return task