from flask import abort, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
import os
import requests

def error_message(message, status_code):
    abort(make_response({"details": message}, status_code))


def validate_id(cls, id):
    try:
        id = int(id)
    except (ValueError, TypeError):
        error_message(f"invalid id {id}", 400)

    model = cls.query.get(id)

    if not model:
        error_message(f"id {id} not found", 404)
    return model


# def form_json_response(model):
#     if type(model) == Task:
#         response = {"task": model.todict()}
#     if type(model) == Goal:
#         response = {"goal": model.todict()}
#     return jsonify(response)


def post_to_slack(task):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": os.environ.get("SLACK_TOKEN")}
    data = {"text": f"Someone completed the task {task.title}",
            "channel": "C03F4FJS013"}
    requests.post(url, data=data, headers=headers)
