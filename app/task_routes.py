from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task 
import datetime

import os
from dotenv import load_dotenv
import requests
load_dotenv()

##for original slack bot soln
# import logging
# logging.basicConfig(level=logging.DEBUG)
# import ssl
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError

def validate_task_id(task_id):
    try: 
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"msg":f"The task with id {task_id} is invalid"}, 400))
    task = Task.query.get(task_id)
    if task:
        return task

    abort(make_response({"msg":f"The task with id {task_id} is not found"}, 404))

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        return make_response({"details": "Invalid data"}), 400

    if "completed_at" in request_body:
        new_task = Task(
            title=request_body["title"], 
            description=request_body["description"], 
            completed_at=request_body["completed_at"], 
            is_complete=True)
    else:
        new_task = Task(
            title=request_body["title"], 
            description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task':
    {'id':new_task.id, 
    'title':new_task.title, 
    'description':new_task.description, 
    'is_complete':new_task.is_complete}
    }), 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(
            task.to_dict_basic()
        )

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task_id(task_id)
    return jsonify(task.to_dict())

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    if task.completed_at:
        task.is_complete = True 
    db.session.commit()

    return jsonify(task.to_dict())

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_task_id(task_id)
    task.completed_at = datetime.datetime.now()
    task.is_complete = True
    db.session.commit()

# create requests.post(slack api)
    slack_url = "https://slack.com/api/chat.postMessage"
    slack_token = os.environ['SLACK_BOT_TOKEN']
    params = {
        "channel": "task-list-api",
        "text": f'Someone just completed the task "{task.title}"'
        }
    headers = {
        "Authorization":"Bearer {}".format(slack_token)
        }
    r = requests.post(slack_url, headers=headers, params=params)

    return jsonify(task.to_dict())

## original soln for slack bot below - keeping in case I need to reference it again... or just cry over how much time I spent trying to figure it out... 
    # ssl_context = ssl.create_default_context()
    # ssl_context.check_hostname = False
    # ssl_context.verify_mode = ssl.CERT_NONE

    # slack_token = os.environ['SLACK_BOT_TOKEN']
    # client = WebClient(token=slack_token, 
    #                     ssl=ssl_context)
    # try:
    #     response = client.chat_postMessage(
    #         channel="task-list-api", 
    #         text=f"Someone just completed the task {task_title}"
    #     )
    # except SlackApiError as e:
    #     assert e.response["error"]


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_task_id(task_id)
    task.completed_at = None
    task.is_complete = False
    db.session.commit()

    return jsonify(task.to_dict())

