from app.models.task import Task
from app.models.goal import Goal
from flask import make_response, jsonify, abort

# validate id either id
def validate_id(model, id):
    try:
        id = int(id)
    except:
        message = f"{model} is invalid"
        return error_message(message, 400)
        
    if model == "Task":
        record = Task.query.get(id)
    elif model == "Goal":
        record = Goal.query.get(id)

    if not record:
        message = f"{model} {id} does not exist"
        return error_message(message, 404)
    return record

def error_message(message, status_code):
    abort(make_response(jsonify({"details":f"{message}"}), status_code))
