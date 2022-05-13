from flask import abort, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal

def error_message(message, status_code):
    abort(make_response({"details": message}, status_code))

def validate_id(cls, id):
    try:
        id = int(id)
    except:
        error_message(f"invalid id {id}", 400)

    model = cls.query.get(id)

    if not model:
        error_message(f"id {id} not found", 404)
    return model


def form_json_response(model):
    if type(model) == Task:
        response = {"task": model.todict()}
    if type(model) == Goal:
        response = {"goal": model.todict()}
    return jsonify(response)