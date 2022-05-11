from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint("bp", __name__, url_prefix="/tasks")

def error_message(message, status_code):
        abort(make_response(jsonify(dict(details=message)), status_code))

def make_task_safely(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)

def replace_task_safely(task, data_dict):
    try:
        task.replace_details(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)

def get_task_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)

    task = Task.query.get(id)
    if task:
        return task
    
    error_message(f"No task with id {id} found", 404)

# POST /tasks
@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = make_task_safely(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

# GET /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_param = request.args.get("sort")

    if sort_param == 'asc':
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_param == 'desc':
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    result_list = [task.to_dict() for task in tasks]

    return jsonify(result_list)

# GET /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["Get"])
def read_task_by_id(task_id):
    task = get_task_record_by_id(task_id)
    return jsonify({"task":task.to_dict()})

# PUT /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_task_by_id(task_id):
    request_body = request.get_json()
    task = get_task_record_by_id(task_id)

    replace_task_safely(task, request_body)

    db.session.add(task)
    db.session.commit()

    return jsonify({"task":task.to_dict()})

# DELETE /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = get_task_record_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

# PATCH /tasks/<task_id>/mark_complete
@tasks_bp.route("/<task_id>/<mark_complete>", methods=["PATCH"])
def update_task_by_id(task_id, completed_at):
    task = get_task_record_by_id(task_id)
    request_body = request.get_json()
    print(request_body)

    # if "is_complete" in task_keys:
    #     task.completed_at = request_body["mark_complete"] 

    db.session.commit()
    return jsonify({"task":task.to_dict()})

