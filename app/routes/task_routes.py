from app import db
from app.models.task import Task
from flask import Blueprint, make_response, request, jsonify
from .helpers import validate_task
import requests, os
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Get all tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()

    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    else:
        tasks = Task.query.all()

    tasks_response = [task.to_json() for task in tasks]
    
    return jsonify(tasks_response),200
    
    # Original code that I wrote for wave 1, before adding lines between 13 ~ 21
    # tasks_response = []
    # if title_query:
    #     tasks = Task.query.filter_by(title=title_query)
    # else:
    #     tasks = Task.query.all()

    # for task in tasks:
    #     tasks_response.append(task.to_json())
    # return jsonify(tasks_response),200


# Get one task
@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return jsonify({"task":task.to_json()}),200

# Create tasks
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try: 
        new_task = Task.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"},400)
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_json()}), 201

# Update tasks
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json()
    task.update(request_body)
    
    db.session.commit()
    
    return jsonify({"task":task.to_json()}), 200

# Delete tasks
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {id} "{task.to_json()["title"]}" successfully deleted'}), 200

# Patch tasks
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def patch_task_to_complete(id):
    task = validate_task(id)
    task.patch_to_complete()

    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"
    query_params = {
        "channel": "brewing",
        "text": f"Someone just completed the task {task.title}"
        }
    headers = {"Authorization": os.environ.get("SLACK_BOT_API_KEY")}

    requests.post(path, params=query_params, headers=headers)
    # requests.post(path, params=query_params, headers=headers), it might work without response_bot variable
    return jsonify({"task":task.to_json()}), 200

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def patch_task_to_incomplete(id):
    task = validate_task(id)
    task.patch_to_incomplete()

    db.session.commit()

    return jsonify({"task":task.to_json()}), 200


