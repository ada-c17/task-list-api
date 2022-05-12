from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import desc
from app import db
from app.models.task import Task
from datetime import date

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# create a new task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task(title=request_body["title"], description=request_body["description"])
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}

    return make_response(jsonify(response_body), 201)

# retrieve all tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_param = request.args.get("sort")

    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_param == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    
    return jsonify(tasks_response)

# retrieve one task by id
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task_by_id(task_id):
    task = validate_task(task_id)

    return {"task": task.to_dict()}

# update one task by id
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task_by_id(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}

# delete one task by id
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})

# mark one task complete by id
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = date.today()
    response_body = {"task": task.to_dict()}

    db.session.commit()
    return make_response(jsonify(response_body), 200)

# mark one task incomplete by id
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    response_body = {"task": task.to_dict()}

    db.session.commit()
    return make_response(jsonify(response_body), 200)

# check for valid task using id
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": f"Task #{task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"details": f"Task #{task_id} not found"}, 404))
    
    return task
