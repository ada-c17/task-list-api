from flask import Blueprint, jsonify, abort, make_response, request
from app import db, slackbot
from app.models.task import Task
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task_or_abort(task_id):
    # returns 400 error if invalid task_id (alpha/non-int) 
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"error": f"{task_id} is an invalid task id"}, 400))
    
    # returns 404 error if task_id not found in database
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"error": f"Task {task_id} not found"}, 404))
    return task


@tasks_bp.route("", methods=["GET"])
def get_saved_tasks():

    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    task_list = []
    for task in tasks:
        task_list.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })
    
    return jsonify(task_list), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_saved_task(task_id):
    task = validate_task_or_abort(task_id)

    return jsonify(task.return_task_dict()), 200


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or\
        "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400        

    if "completed_at" in request_body:
        completed_status = request_body["completed_at"]
    else:
        completed_status = None

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=completed_status
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.return_task_dict()), 201


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_saved_task(task_id):
    task = validate_task_or_abort(task_id)
    
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]

    db.session.commit()

    return jsonify(task.return_task_dict()), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task_or_abort(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_task_or_abort(task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()

    slackbot.post_to_slack(task)

    return make_response(jsonify(task.return_task_dict()), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_task_or_abort(task_id)

    task.completed_at = None

    db.session.commit()
    
    return jsonify(task.return_task_dict()), 200