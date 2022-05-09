from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix='/tasks')

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"msg": f"Invalid Id: '{task_id}'. ID must be an integer."}, 400))

    chosen_task = Task.query.get(task_id)

    if not chosen_task:
        abort(make_response({"msg": f"Task {task_id} not found"}, 404))

    return chosen_task

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args

    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })

    # there probably is way to query by sorted
    if "sort" in params:
        if params["sort"] == "asc":
            tasks_response = sorted(tasks_response, key = lambda d: d["title"])
        elif params["sort"] == "desc":
            tasks_response = sorted(tasks_response, key = lambda d: d["title"], reverse=True)
    
    return jsonify(tasks_response)

@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({
            "details": "Invalid data"
            }), 400

    if "completed_at" in request_body:
        new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=datetime.utcnow())
    else:
        new_task = Task(title=request_body["title"], description=request_body["description"])

    
    db.session.add(new_task)
    db.session.commit()

    if new_task.completed_at:
        return jsonify({
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": True
        }
    }), 201

    return jsonify({
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }), 201

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

    chosen_task = validate_task(task_id)

    return jsonify({
        "task": {
            "id": chosen_task.id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": False
            }
    })


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    chosen_task = validate_task(task_id)

    if "title" not in request_body or\
        "description" not in request_body:
        return jsonify({"msg": "Request must include title and description."}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]

    if "completed_at" in request_body:
        chosen_task.completed_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "task": {
                "id": chosen_task.id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": True
            }
        })

    db.session.commit()

    return jsonify({
        "task": {
            "id": chosen_task.id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": False
        }
    })

@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = validate_task(task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    return jsonify({
        "details": f"Task {chosen_task.id} \"{chosen_task.title}\" successfully deleted"
    })

@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    chosen_task = validate_task(task_id)

    chosen_task.completed_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "task": {
            "id": chosen_task.id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": True
        }
    })

@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    chosen_task = validate_task(task_id)

    chosen_task.completed_at = None
    db.session.commit()

    return jsonify({
        "task": {
            "id": chosen_task.id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": False
        }
    })