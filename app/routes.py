from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_one_task():
    if not request.is_json:
        return {"msg" : "Missing JSON request body"}, 400
    
    request_body = request.get_json()
    try:
        title = request_body["title"]
        description = request_body["description"]
    except KeyError:
        return {"details": "Invalid data"}, 400

    new_task = Task(title=title,
                description=description,
                completed_at=None)

    db.session.add(new_task)
    db.session.commit()
    
    rsp = {"task" : new_task.get_dict()}

    return jsonify(rsp), 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.get_dict())
    
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    rsp = {"task" : task.get_dict()}

    return jsonify(rsp), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    if not request.is_json:
        return {"msg" : "Missing JSON request body"}, 400

    request_body = request.get_json()
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except KeyError:
        return {
            "msg" : "Update failed due to missing data. Title, Description are required!"
        }, 400

    db.session.commit()

    rsp = {"task" : task.get_dict()}
    return jsonify(rsp), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    rsp = {"details": f'Task {task_id} "{task.title}" successfully deleted'}
    return jsonify(rsp), 200






def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        rsp = {"msg" : f"Task with id #{task_id} is invalid."}
        abort(make_response(rsp, 400))
    
    task = Task.query.get(task_id)

    if not task:
        rsp = {"msg" : f"Task with id #{task_id} is not found!"}
        abort(make_response(rsp, 404))
    return task


