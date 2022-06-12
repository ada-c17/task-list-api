from datetime import datetime
from typing import OrderedDict
from urllib.request import OpenerDirector
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task

### Create a Task:
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()
    if "title" in request_body and "description" in request_body and "completed_at" in request_body:
        new_task = Task( 
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"]
            )
    elif "title" in request_body and "description" in request_body:
        new_task = Task( 
            title = request_body["title"],
            description = request_body["description"],
            # completed_at = request_body["completed_at"]
            )
    else:
        return jsonify({"details":"Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()
    task_response = {"task": new_task.to_dictionary()}
    return (jsonify(task_response), 201)


### Get Tasks
@tasks_bp.route("", methods = ["GET"])
def get_tasks():
    sort = request.args.get("sort")
    #Sort by assending (is default?)
    if sort == "asc":
        tasks =Task.query.order_by(Task.title)
    #Sort by decending
    elif sort == "desc":
        tasks =Task.query.order_by(Task.title.desc())
    #No Sort
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dictionary())
        # If No Saved Tasks wil stil return 200
    return (jsonify(tasks_response), 200)


### Get One Task: One Saved Task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    task_response = {"task": task.to_dictionary()}
    return (jsonify(task_response), 200)


### Update Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    task_response = {"task": task.to_dictionary()}
    return (jsonify(task_response), 200)

# Task Complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def task_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.utcnow()
    
    db.session.commit()
    task_response = {"task": task.to_dictionary()}
    return (jsonify(task_response), 200)

# Task Incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def task_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    task_response = {"task": task.to_dictionary()}
    return (jsonify(task_response), 200)


# Delete Task: Deleting a Task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}
    return (jsonify(response), 200)


# Validate there are no matching Task: Get, Update, and Delete

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} is invalid"}, 400))


    task = Task.query.get(task_id)
    
    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))
    return task













