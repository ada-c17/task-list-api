from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from datetime import datetime



tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_msg = {"message": f'{task_id} id is not valid, must be an integer'}
        abort(make_response(jsonify(response_msg), 400))
    the_task = Task.query.get(task_id)

    if the_task is None:
        response_msg = {"message": f'task with id {task_id} not found'}
        abort(make_response(jsonify(response_msg), 404))
    return the_task

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    if "completed_at" in request_body: 
    # /and isinstance(request_body["completed_at"], datetime.date):
        new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"],
                    is_complete=True)
    else:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()


    return make_response(jsonify({"task":{
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.is_complete
    }
    }), 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    param = request.args.get("sort")
    
    tasks_response = []
    
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    if param == "asc":
        tasks_response = sorted(tasks_response, key=lambda d: d["title"])
    if param == "desc":
        tasks_response = sorted(tasks_response, key=lambda d: d["title"], reverse=True)
    
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):

    task = validate_task_id(task_id)

    return jsonify({"task":{

        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete
        }})
    
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)

    request_body = request.get_json()

    if "completed_at" in request_body: 
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]
        task.is_complete = True
    
    else:
        task.title = request_body["title"]
        task.description = request_body["description"]
    # task.completed_at = request_body["completed_at"]
    # task.is_complete = request_body["is_complete"]

    db.session.commit()

    return jsonify({"task":{
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete
        }})

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()

    task_deleted = f'Task {task.task_id} "{task.title}" successfully deleted'

    return make_response({"details": task_deleted})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    
    task = validate_task_id(task_id)


    task.completed_at = datetime.utcnow()
    task.is_complete = True

    db.session.commit()
    
    task_updated = {"task": {
    "id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": task.is_complete
                            }
                    }
    return make_response(jsonify(task_updated), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task_id(task_id)

    task.completed_at = None
    task.is_complete = False

    db.session.commit()

    task_updated = {"task": {
    "id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": task.is_complete
                            }
                    }

    return make_response(jsonify(task_updated),200)