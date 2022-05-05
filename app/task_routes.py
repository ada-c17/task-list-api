from asyncio import all_tasks
from xxlimited import new
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("Tasks", __name__, url_prefix="/tasks")

# Helper functions

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def success_message(message, status_code=200):
    return make_response(jsonify(dict(task=message)), status_code)

def return_database_info(return_value):
    return make_response(jsonify(return_value))

def get_task_by_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id: {id}", 400)
    task = Task.query.get(id)
    if task:
        return task
    else:
        error_message(f"Task id: {id} not found", 404)

def create_task_safely(data_dict):
    try:
        return Task.create_from_dict(data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s):{err}. Task not added to task list.", 400)
    except KeyError as err:
        error_message(f"Missing key(s): {err}.  Task not added to task list.", 400)



# Route functions

@task_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    new_task = create_task_safely(request_body)

    db.session.add(new_task)
    db.session.commit()

    return success_message(new_task.self_to_dict(), 201)

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    
    all_tasks = [task.self_to_dict() for task in tasks]

    return return_database_info(all_tasks)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_task_by_id(task_id)
    return return_database_info(dict(task=task.self_to_dict()))