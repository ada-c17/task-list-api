from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix='/tasks')


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    
    return jsonify(tasks_response)

@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({
            "details": "Invalid data"
            }), 400

    new_task = Task(title=request_body["title"], description=request_body["description"])
    
    db.session.add(new_task)
    db.session.commit()

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


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"msg": f"Invalid Id: '{task_id}'. ID must be an integer."}, 400))

    chosen_task = Task.query.get(task_id)

    if not chosen_task:
        abort(make_response({"msg": f"Task {task_id} not found"}, 404))

    return chosen_task