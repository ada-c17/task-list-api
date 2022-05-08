from flask import abort, make_response
from .models.task import Task

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} is not a valid id"}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"message": f"Task {id} not found"}, 404))

    return task