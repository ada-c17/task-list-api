from flask import Blueprint, jsonify, abort, make_response, request
from requests import session
from app.helpers import validate_task
from app.models.task import Task
from app import db
from .helpers import validate_task
from datetime import datetime
import requests, os



# TASK BLUEPRINT
'''
Blueprints are a Flask class that provides a pattern 
for grouping related routes (endpoints)
'''

task_bp = Blueprint("task", __name__, url_prefix = "/tasks")



# Create a Task: Valid Task With null completed_at

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    if "description" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    

    new_task = Task.create(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_json()}),201)


# Get Tasks

@task_bp.route("", methods=["POST", "GET"])
def get_all_tasks():
    title_query=request.args.get("sort")

    # description_query=request.args.get("description")

    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else: 
        tasks = Task.query.all()
    
    # tasks_response = [task.to_dict() for task in tasks]

    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200




# Get One Task: One Saved Task
@task_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)
    return jsonify({"task":task.to_json()}), 200


# Update Task
@task_bp.route("/<id>", methods=["PUT"])
def update_task(id): 
    task = validate_task(id)
    request_body = request.get_json()

    task.update(request_body)
    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}),200)


# Delete Task: Deleting a Task
@task_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {id} \"{task.title}\" successfully deleted"}))

# Mark Complete
@task_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_task(id)

    task.completed_at = datetime.utcnow()

    db.session.commit()
    post_message_to_slack(task)

    return make_response(jsonify({"task": task.to_json()})), 200

def post_message_to_slack(task):
    send_msg_path = "https://slack.com/api/chat.postMessage"
    confirm_message = f"You completed the task {task.title}!"
    query_params = {
        "channel":"task-notifications",
        "text": confirm_message
        } 
    headers = {
        "Authorization": os.environ.get("slack_token")
        }
    requests.post(send_msg_path, params=query_params, headers=headers)



# Mark Incomplete 
@task_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_task(id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task": task.to_json()})), 200








    

