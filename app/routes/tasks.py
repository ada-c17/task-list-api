import requests
#from requests_oauthlib import OAuth1
import os
from dotenv import load_dotenv
from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import date
from app.models.task import Task

load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def handle_id_request(id):
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid Task ID '{id}'."}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"msg": f"Task ID '{id}' does not exist."}, 404))

    return task

def check_complete_request_body(request):
    request_body = request.get_json()
    if all(element in request_body for element in Task.expected_elements):
        if all(type(request_body[element]) == Task.expected_elements[element] \
                    for element in Task.expected_elements):
                        return request_body
    abort(make_response({"details": "Invalid data"}, 400))

def slack_complete(task):
    url = "https://slack.com/api/chat.postMessage"
    slack_message = f"{task.title} was completed! \U0001F4AF"

    query_params = {
        "channel": "task-completion",
        "text": slack_message
    }
    auth_token = os.environ.get("SLACKBOT_API_TOKEN")
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(url, params=query_params, headers=headers)
    return response


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    query_params = request.args
    if "sort" in query_params:
        if query_params["sort"] == "asc":
            task_list = Task.query.order_by(Task.title.asc()).all()
        elif query_params["sort"] == "desc":
            task_list = Task.query.order_by(Task.title.desc()).all()
        #care here -- if something not asc or desc in query_params["sort"]
        #task_list will not exist
    else: 
        task_list = Task.query.all()

    task_response = []

    for task in task_list:
        task_response.append(task.make_response_dict())
    
    return make_response(jsonify(task_response), 200)

@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = check_complete_request_body(request)
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
    )

    if request_body.get("completed_at"):
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    confirmation_msg = {"task": new_task.make_response_dict()}

    return make_response(jsonify(confirmation_msg), 201)

@tasks_bp.route("/<id>", methods=["GET"])
def get_task_by_id(id):
    task = handle_id_request(id)
    confirmation_msg = {"task": task.make_response_dict()}
    return make_response(jsonify(confirmation_msg), 200)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task_by_id(id):
    request_body = check_complete_request_body(request)
    task_to_update = handle_id_request(id)

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return make_response(
        jsonify({"task": task_to_update.make_response_dict()}),
        200
        )


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task_by_id(id):
    task = handle_id_request(id)
    db.session.delete(task)
    db.session.commit()

    return make_response(
            jsonify({"details": f"Task {id} \"{task.title}\" successfully deleted"}), 
            200
            )

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task = handle_id_request(id)
    task.completed_at = date.today()
    db.session.commit()

    confirmation_msg = {"task": task.make_response_dict()}

    slack_response = slack_complete(task)

    #confirmation_msg["slack-response"] = slack_response.json()
    #for troubleshooting response from Slack API through postman
    return make_response(jsonify(confirmation_msg), 200)

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task = handle_id_request(id)
    task.completed_at = None
    db.session.commit()

    confirmation_msg = {"task": task.make_response_dict()}

    return make_response(jsonify(confirmation_msg), 200)