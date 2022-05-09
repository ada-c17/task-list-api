from flask import request, make_response, abort
from app.models.task import Task
from app.models.goal import Goal

def validate_element(element_id):
    try:
        element_id = int(element_id)
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    if request.blueprint == "tasks":
        element = Task.query.get(element_id)
        name = "Task"
    elif request.blueprint == "goals":
        element = Goal.query.get(element_id)
        name = "Goal"

    if not element:
        return abort(make_response({"message" : f"{name} {element_id} is not found"}, 404))
    return element