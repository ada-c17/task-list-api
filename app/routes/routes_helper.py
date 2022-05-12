# from app import db
from flask import jsonify, make_response, abort
from ..models.task import Task
from ..models.goal import Goal
import requests, os

def success_response(message, status_code):
    return make_response(jsonify(message), status_code)

def error_response(message, status_code):
    abort(make_response(message, status_code))

def validate_item(cls, id):
    try:
        id = int(id)
    except:
        error_response({"message": f"{cls.__name__} {id} invalid"}, 400)

    item = cls.query.get(id)
#check item is found
    if not item:
        error_response({"message": f"{cls.__name__} {id} not found"}, 404)
    else:
        return item

def post_completed_task_to_slack(task_title):
    path = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_TOKEN")

    headers = {"Authorization": f"Bearer {SLACK_API_KEY}",
    "Content-Type": "application/json"}
    json_body = {"channel": "task-notifications",
    "text": f"Someone just completed the task {task_title}"}

    requests.post(path, headers=headers, json=json_body)
