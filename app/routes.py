from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    '''Validates that task id is valid and exists'''
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"msg": f"Invalid id: {task_id}"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"msg": f"Could not find task with id: {task_id}"}, 404))

    return task

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"], 
                        description=request_body["description"])
    except KeyError:
        return {"details": "Invalid data"}, 400

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

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = request.args
    
    if task_query and task_query["sort"] == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif task_query and task_query["sort"] == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
        })
    return jsonify(tasks_response)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return { 
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at = request_body["is_complete"]
    
    db.session.commit()
    
    return { 
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}
