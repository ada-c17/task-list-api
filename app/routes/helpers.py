from app.models.task import Task
from flask import make_response, abort

def validate_task(id):
    try:
        id = int(id)
    except:
        return abort(make_response({"message": f"task {id} is invalid"}, 400))


    task = Task.query.get(id)
    if not task:
        abort(make_response({"message": f"task {id} not found"},404))
    
    return task
