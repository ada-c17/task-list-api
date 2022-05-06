from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response(jsonify({'details': 'Invalid data'}), 400))

    task = Task.query.get(task_id)

    if not task:
        return abort(make_response(jsonify(f"Task {task_id} not found"), 404))
    
    return task


@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"]
        )

        db.session.add(new_task)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.commit()
    
    task = Task.query.get(int(new_task.task_id))
    is_complete = bool(task.completed_at)

    return make_response({"task": task.to_dict(is_complete)}, 201)

@bp.route("", methods=["GET"])
def read_all_tasks():
    title_param = request.args.get("title")
    description_param = request.args.get("description")
    completed_at_param = request.args.get("completed_at")

    tasks = Task.query

    if title_param:
        tasks = tasks.filter_by(title=title_param)
    if description_param:
        tasks = tasks.filter_by(description=description_param)
    if completed_at_param:
        tasks = tasks.filter_by(completed_at=completed_at_param)
    
    tasks = tasks.all()

    tasks_response = []
    for task in tasks:
        is_complete = bool(task.completed_at)

        tasks_response.append(task.to_dict(is_complete))

    return jsonify(tasks_response)

@bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    is_complete = bool(task.completed_at)
    
    return {"task": task.to_dict(is_complete)}

@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    is_complete = bool(task.completed_at)

    db.session.commit()

    return {"task": task.to_dict(is_complete)}

@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'details': f'Task "{task.title}" successfully deleted'})