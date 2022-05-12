
from app.models.task import Task
from app.models.goal import Goal
from flask import abort, make_response

def validate_task(id):
    try:
        id = int(id)
    except:
        return abort(make_response({"message": f"task {id} is invalid"}, 400))
    
    task = Task.query.get(id)

    if not task:
        abort(make_response({"message": f"task {id} not found"}, 404))

    return task

def validate_goal(id):
    try:
        id = int(id)
    except:
        return abort(make_response({"message": f"goal {id} is invalid"}, 400))
    
    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message": f"goal {id} not found"}, 404))

    return goal