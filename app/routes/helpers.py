from app.models.task import Task
from app.models.goal import Goal
from flask import make_response, jsonify, abort

# validate id either id
def validate_id(model, id):
    try:
        id = int(id)
    except:
        return abort(make_response(jsonify(f"{model} is invalid"), 400))

    if model == "Task":
        record = Task.query.get(id)
    elif model == "Goal":
        record = Goal.query.get(id)

    if not record:
        return abort(make_response(jsonify(f"{model} {id} does not exist"), 404))
    return record
