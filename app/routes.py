from flask import Blueprint, jsonify, make_response, abort, request
from app.models.task import Task
from app import db
# helper function file import

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")  # what is string "task_bp", why do we need

# CREATE TASK - "POST"
# WE NEED TO TRY THIS
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()  # this is from request pckg
    new_task = Task.create(request_body)   # create decorator from Task model

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task {new_task.title} successfully created", 201)

#GET SAVED TASKS - "GET" (all)
@task_bp.route("", methods=["GET"])
def read_saved_tasks():
    # if we have query parameters
    # title_query = request.args.get("title")
    # if title_query:
    #     tasks = Task.query.filter_by(title=title_query)
    # else:
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
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        return abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task

# GET ONE TASK
@task_bp.route("/<task_id>", methods=["GET"])  # spaces or no spaces
def read_one_task(task_id):
    task = validate_task(task_id)

    return jsonify(task.to_json(), 200)   # to_json is our function in class - how does it know to get tehre

# UPDATE ONE TASK
@task_bp.route("/<task_id>", methods = ["PUT"])
def update_one_planet(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.update(request_body)
    db.session.commit()

    return make_response(jsonify(f"Task # {task.task_id} successfully updated"), 200)

# DELETE ONE TASK
@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task # {task.id} successfully deleted"), 200


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
