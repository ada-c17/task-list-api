from flask import Blueprint, jsonify, make_response, abort, request
from app.models.task import Task
from app import db
# helper function file import
from sqlalchemy import asc, desc
from datetime import datetime

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")  # what is string "task_bp", why do we need


'''
POST ROUTE
'''

# CREATE TASK
# LOCALHOST
# without create decorator from Task model
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()  # this is from request pckg

    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    if "description" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)

    new_task = Task(title=request_body["title"], description=request_body["description"])

    if "completed_at" in request_body:
        new_task.completed_at = datetime.utcnow()

    db.session.add(new_task)
    db.session.commit()

    task_response_body = {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at),
    }
    return make_response(jsonify({"task": task_response_body}), 201)


'''
GET ROUTES
'''

# def sort_ascending(listofdicts, key):
#     sorted_dict = sorted(listofdicts, key=lambda d: d[key])
#     return sorted_dict


# GET SAVED TASKS - (all)
@task_bp.route("", methods=["GET"])
def read_saved_tasks():


    # query params
    title_sort_query = request.args.get("sort")
    if title_sort_query == "asc":
        print("hello")
        tasks = Task.query.order_by(asc(Task.title)).all()
    elif title_sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()

    tasks_response = []

    for task_dict in tasks:   # tasks in line 29
        # since we use jsonify, i wonder if I omit the dictionary part
        # if it will still turn it into a dict, but we are in a loop
        tasks_response.append(
            {
                "id": task_dict.task_id,
                "title": task_dict.title,
                "description": task_dict.description,
                "is_complete": bool(task_dict.completed_at)
            }
        )
    return jsonify(tasks_response)   # we turn this Python list into a json collection
                                    # is it an obj/dict

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        return abort(make_response({"details": f"Task {task_id} not found"}, 404))

    return task

# GET ONE TASK
@task_bp.route("/<task_id>", methods=["GET"])  # spaces or no spaces
def read_one_task(task_id):
    task = validate_task(task_id)

    task_response_body = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at),
    }
    return make_response(jsonify({"task": task_response_body}), 200)

'''
PUT ROUTES
'''

# UPDATE ONE TASK
# without update function in task.py
@task_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    # task.update(request_body)
    db.session.commit()

    task_response_body = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at),
    }

    return make_response(jsonify({"task": task_response_body}), 200)

'''
PATCH ROUTE
'''

# PATCH ONE TASK - MARK COMPLETE
@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def patch_task_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.utcnow()

    # task.update(request_body)
    db.session.commit()

    task_response_body = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at),
    }

    return make_response(jsonify({"task": task_response_body}), 200)

# PATCH ONE TASK - MARK INCOMPLETE
@task_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def patch_task_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None

    # task.update(request_body)
    db.session.commit()

    task_response_body = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at),
    }

    return make_response(jsonify({"task": task_response_body}), 200)


'''
DELETE ROUTE
'''

# DELETE ONE TASK
@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    delete_response = f"Task {task.task_id} \"{task.title}\" successfully deleted"

    return make_response(jsonify({"details": delete_response}), 200)

# =========

# Hello TASK JUST TO CHECK
@task_bp.route("", methods=["GET"])
def say_hello_task():
    response_body = "THIS IS OUR TASK!"
    return response_body, 200

# Hello TASK JSON JUST TO CHECK
@task_bp.route("/JSON", methods=["GET"])
def hello_task_json():
    task = {
        "task_id": 1,
        "title": "Clean dishes",
        "description": "We want all dishes cleaned, dishwasher started",
        "completed_at": True
    }

    return task, 200
