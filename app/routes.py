from flask import Blueprint, jsonify, make_response, abort, request
from app.models.task import Task
from app import db
# helper function file import
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


'''
POST ROUTE
'''

# CREATE TASK
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

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

# GET SAVED TASKS - ALL, QUERY PARAMS
@task_bp.route("", methods=["GET"])
def read_saved_tasks():

    title_sort_query = request.args.get("sort")

    if title_sort_query == "asc":
        print("hello")
        tasks = Task.query.order_by(asc(Task.title)).all()
    elif title_sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()

    tasks_response = []

    for task_dict in tasks:
        tasks_response.append(
            {
                "id": task_dict.task_id,
                "title": task_dict.title,
                "description": task_dict.description,
                "is_complete": bool(task_dict.completed_at)
            }
        )
    return jsonify(tasks_response)

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
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)

    # return make_response(jsonify(task.to_json()), 200)
    return make_response(jsonify({"task": task.to_json()}), 200)

'''
PUT ROUTES
'''

# UPDATE ONE TASK
# without update function in task.py
@task_bp.route("/<task_id>", methods=["PUT"])
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
PATCH ROUTES
'''

# PATCH ONE TASK - MARK COMPLETE
@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def patch_task_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.utcnow()

    '''
    Nested request - sends a post request to my Slackbot to send a
    message about the task that's just been completed
    '''
    call_slackbot(task)

    db.session.commit()

    task_response_body = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at),
    }

    return make_response(jsonify({"task": task_response_body}), 200)


# HELPER FUNCTION THAT SENDS A POST REQUEST TO SLACKBOT FOR PATCH METHOD
def call_slackbot(tasky):
    response1 = requests.post(
        "https://slack.com/api/chat.postMessage",
        params={
            "channel": "task-notifications",
            "text": f"Someone just completed the task {tasky.title}"
        },
        headers={
            "Authorization": os.environ.get("SLACK_AUTH")
        }
    )

    # return response1
    return response1.json()

# PATCH ONE TASK - MARK INCOMPLETE
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
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
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    delete_response = f"Task {task.task_id} \"{task.title}\" successfully deleted"

    return make_response(jsonify({"details": delete_response}), 200)
