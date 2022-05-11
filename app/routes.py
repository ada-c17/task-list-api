from turtle import title
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task 
from app import db

bp = Blueprint("tasks_bp",__name__, url_prefix="/tasks")

# helper functions
def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def get_task_record_by_id(id):
    try: 
        id = int(id)
    except ValueError:
        error_message(f"Invalid task id {id}", 400)
    
    task = Task.query.get(id)

    if task:
        return task
    
    error_message(f"No task with id {id} found", 404)

# POST /tasks
@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        task = Task.from_dict(request_body)
    except KeyError:
        error_message(f"Invalid data", 400)

    db.session.add(task)
    db.session.commit()

    return jsonify({"task": task.make_dict()}), 201

# GET /tasks?sort=
@bp.route("", methods=["GET"])
def list_tasks():
    sort_param = request.args.get("sort")
    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    list_of_tasks = [task.make_dict() for task in tasks]

    return jsonify(list_of_tasks)


# GET /tasks/<task_id>
@bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = get_task_record_by_id(task_id)

    return jsonify({"task": task.make_dict()})

# PUT /tasks/<task_id>
@bp.route("/<task_id>", methods=["PUT"])
def replace_task_by_id(task_id):
    request_body = request.get_json()
    task = get_task_record_by_id(task_id)

    try: 
        task.replace_all_details(request_body)
    except KeyError as error:
        error_message(f"Missing key: {error}", 400)

    db.session.commit()

    return jsonify({"task": task.make_dict()})

# PATCH  /tasks/<task_id>/mark_complete
@bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task_by_id(task_id):
    task = get_task_record_by_id(task_id)

    task.mark_complete()

    db.session.commit()

    return jsonify({"task": task.make_dict()})

# PATCH  /tasks/<task_id>/mark_incomplete
@bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task_by_id(task_id):
    task = get_task_record_by_id(task_id)

    task.mark_incomplete()

    db.session.commit()

    return jsonify({"task": task.make_dict()})

# DELETE /tasks/<task_id>
@bp.route("/<task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = get_task_record_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    task = task.make_dict()
    return jsonify({'details': f'Task {task_id} "{task["title"]}" successfully deleted'})