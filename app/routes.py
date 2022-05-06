from flask import Blueprint, request,jsonify, make_response
from app.models.task import Task
from app import db 

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        return {"details": "Invalid data"}, 400


    new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }, 201

def is_complete(task):
    if not task.completed_at:
        return False 
    else:
        return True 

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"message": f"Could not retrieve task with id {task_id}"} 
        return response, 404
    
    task = Task.query.get(task_id)

    if task is None:
        response = {"message": f"Invalid ID: {task_id}"}
        return response, 400 
    
    return task 

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_task(task_id)

    return make_response(jsonify({
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_complete(task)
            }
    })), 200

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []

    if len(tasks) == 0:
        return jsonify(tasks_response), 200

    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete(task)
        })
    
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    # updated_task = None
    if "title" and "description" in request_body:
        # updated_task.title = request_body["title"]
        # updated_task.description = request_body["description"]
        task.title = request_body["title"]
        task.description = request_body["description"]
    
    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete(task)
        }
    }, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }), 200