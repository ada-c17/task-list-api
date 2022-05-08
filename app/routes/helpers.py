from flask import abort, make_response
from ..models.task import Task
from ..models.goal import Goal

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} is not a valid id"}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"message": f"Task {id} not found"}, 404))

    return task

def validate_goal(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} is not a valid id"}, 400))

    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message": f"Goal {id} not found"}, 404))

    return goal