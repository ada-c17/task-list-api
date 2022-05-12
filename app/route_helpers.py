from app.models.task import Task
from flask import jsonify, abort, make_response
def fetch_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify({"details":f"invalid data"}), 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify({"details": f"task {task_id} not found"}), 404))
    return task