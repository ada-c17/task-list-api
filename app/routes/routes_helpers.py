from app.models.task import Task
from app.models.goal import Goal
from flask import make_response, jsonify, abort
import os
import requests

# validate id either id
def validate_id(model, id):
    try:
        id = int(id)
    except:
        message = f"{model} is invalid"
        return error_message(message, 400)
        
    if model == "Task":
        record = Task.query.get(id)
    elif model == "Goal":
        record = Goal.query.get(id)

    if not record:
        message = f"{model} {id} does not exist"
        return error_message(message, 404)
    return record

def error_message(message, status_code):
    abort(make_response(jsonify({"details":f"{message}"}), status_code))

def send_msg_to_channel(task):
    send_msg_path = "https://slack.com/api/chat.postMessage"
    confirm_message = f"Someone just completed the task {task.title}!"
    query_params = {
        "channel":"task-notifications",
        "text": confirm_message
        } 
    headers = {
        "Authorization": os.environ.get("SLACK_OAUTH_TOKEN")
        }
    requests.post(send_msg_path, params=query_params, headers=headers)