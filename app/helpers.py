from flask import make_response, abort
from app.models.task import Task
from app.models.goal import Goal


def validate_task(id):
    try:
        id = int(id)
    except:
        return abort(make_response({"details": f"Task is invalid"}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"details": f"Task 1 not found"}, 404))

    return task


def validate_goal(id):
    try:
        id = int(id)
    except:
        abort(make_response({"details": f"Goal is invalid"}, 400))

    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"details": f"Goal 1 not found"}, 404))
    return goal
