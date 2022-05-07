from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
from sqlalchemy import desc, asc
from datetime import datetime 

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"])
        new_task.title = request_body["title"]
        new_task.description = request_body["description"]
        
    except KeyError:
        return {
            "details": "Invalid data"
        } , 400

    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()
    
    response = jsonify({"task": {
        "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": bool(new_task.completed_at)}
    })
    return response, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args
    if "sort" in params :
        if params["sort"] == "desc":
            tasks = Task.query.order_by(desc(Task.title)).all()
        else:
            tasks = Task.query.order_by(asc(Task.title)).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    return jsonify(tasks_response), 200

def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"details": f"Invalid id: {task_id}"}
        abort(make_response(jsonify(response),400))
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        response = {"details": f"Could not find task with id #{task_id}"}
        abort(make_response(jsonify(response),404))
    return chosen_task

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    response = jsonify({"task": {
        "id": chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)}
    })
    return response, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    request_body = request.get_json()

    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
        
    
    except KeyError:
        return {
            "details": "title, description are required"
        } , 400

    try:
        chosen_task.completed_at = request_body["completed_at"]

    except KeyError:
        pass

    db.session.commit()
    response = jsonify({"task": {
        "id": chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)}
    })
    return response, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    chosen_task.completed_at = datetime.utcnow()

    db.session.commit()
    response = jsonify({"task": {
        "id": chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)}
    })
    return response, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    
    chosen_task.completed_at = None

    print (chosen_task)

    db.session.commit()
    response = jsonify({"task": {
        "id": chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)}
    })

    return response, 200



@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f'Task {chosen_task.task_id} "{chosen_task.title}" successfully deleted'
    }, 200