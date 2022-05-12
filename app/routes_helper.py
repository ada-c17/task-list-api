from flask import jsonify, make_response, abort
from app.models.task import Task

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        create_message("Invalid data", 400)

    task = Task.query.get(task_id)

    if not task:
        create_message("Task 1 not found", 404)
    return task


def create_message(details_info, status_code):
    abort(make_response({"details": details_info}, status_code))