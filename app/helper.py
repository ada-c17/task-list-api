from flask import abort, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"error_message": f"ivalid id {task_id}"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"error_message": f"id {task_id} not found"}, 404))
    return task


def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"error_message": f"ivalid id {id}"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response({"error_message": f"id {id} not found"}, 404))
    return model


def form_json_response(model):
    if type(model) == Task:
        response = {"task": model.todict()}
    if type(model) == Goal:
        response = {"goal": model.todict()}
    return jsonify(response)
