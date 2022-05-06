from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response(f"Task {task_id} is invalid", 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response(f"Task {task_id} not found", 404))
    
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
        abort(make_response(jsonify({
            "description": "Invalid data"
            }), 400))

    db.session.commit()
    
    task = Task.query.get(int(new_task.task_id))

    return make_response(jsonify({"task": {
    "id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": task.is_complete
  }
}
    ), 201)

@bp.route("", methods=["GET"])
def read_all_tasks():
    title_param = request.args.get("title")
    description_param = request.args.get("description")
    completed_at_param = request.args.get("completed_at")
    is_complete_param = request.args.get("is_complete")

    tasks = Task.query

    if title_param:
        tasks = tasks.filter_by(title=title_param)
    if description_param:
        tasks = tasks.filter_by(description=description_param)
    if is_complete_param:
        tasks = tasks.filter_by(is_complete=is_complete_param)
    if completed_at_param:
        tasks = tasks.filter_by(completed_at=completed_at_param)
    
    tasks = tasks.all()

    tasks_response = []
    for task in tasks:
        if task.is_complete == 'False':
            complete_as_bool = False
        else:
            complete_as_bool = True
        
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": complete_as_bool
            }
        )
    return jsonify(tasks_response)

@bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    
    return {"task": task.to_dict()}

@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return task.to_dict()

@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    
    return jsonify(f'Task \{task.title}\ successfully deleted')