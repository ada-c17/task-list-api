from flask import abort, make_response
from app.models.task import Task

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"error_message": f"ivalid id {task_id}"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"error_message": f"id {task_id} not found"}, 404))
    return task

def validate(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"error_message": f"ivalid id {id}"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response({"error_message": f"id {id} not found"}, 404))
    return model