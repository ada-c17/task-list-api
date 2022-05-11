from .task import Task
from flask import abort, make_response

def validate_id(task_id):
    try:
        task_id = int(task_id)
    except:
        return abort(make_response({"message": f"Task {task_id} is not valid"}, 400))
    task = Task.query.get(task_id)
    if not task:
        return abort(make_response({"message": f"Task {task_id} does not exist"}, 404))

    return task

def validate_data(request_body):
    if 'title' not in request_body:
        return abort(make_response(f"Invalid data"),400)
    elif 'description' not in request_body:
        return abort(make_response(f"Invalid data"),400)