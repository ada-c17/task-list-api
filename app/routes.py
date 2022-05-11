from flask import Blueprint
from os import abort
from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from sqlalchemy import asc, desc
import datetime


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

#CREATE 
@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    if "title" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    if "description" not in request_body:
        return {
            "details": "Invalid data"
        }, 400

    if "completed_at" not in request_body:
        completed_at = None
    else:
        completed_at = request_body["completed_at"]
    
    new_task = Task(
                title=request_body["title"],
                description=request_body["description"],
                completed_at=completed_at)


    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }
    }, 201 

#READ

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    param = request.args
    if "sort" in param:
        if param["sort"] == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif param["sort"] == "desc":
            tasks = Task.query.order_by(Task.title.desc())
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



@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    
    response = { "task": {
                "id" : chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)
                }
            }
    return jsonify(response), 200



#UPDATE
@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    request_body = request.get_json()

    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
        
    except KeyError:
        return {
            "details": "Invalid data"
        } , 400

    db.session.commit()

    return { "task": {
                "id" : chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)
                }
            }
    return jsonify(response), 200



@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def completed_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    # request_body = request.get_json()

    # chosen_task.title = request_body["title"]
    # chosen_task.description = request_body["description"]
    # chosen_task.completed_at = request_body["is_complete"]

    chosen_task.completed_at = datetime.datetime.utcnow()
# 
    db.session.add(chosen_task)
    db.session.commit()


    return { "task": {
                "id" : chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)
                }
            }
    return jsonify(response), 200




@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incompleted_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    # request_body = request.get_json()

    # chosen_task.title = request_body["title"]
    # chosen_task.description = request_body["description"]
    # chosen_task.completed_at = request_body["is_complete"]
    chosen_task.completed_at = None

    db.session.add(chosen_task)
    db.session.commit()

    return { "task": {
                "id" : chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at)
                }
            }
    return jsonify(response), 200





#DELETE
@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f"Task {chosen_task.task_id} \"Go on my daily walk 🏞\" successfully deleted" }, 200



#helper function to handle invalid task id and no task in DB
def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response),400))

    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        response = {"message":f"Could not find task with id {task_id}"}
        abort(make_response(jsonify(response),404))
    return chosen_task