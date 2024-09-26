from app.models.task import Task
from app.models.goal import Goal
from flask import make_response, jsonify, abort
from sqlalchemy import asc,desc
import os
import requests

# validate id either id
def validate_id(cls, id):
    try:
        id = int(id)
    except:
        message = f"{cls.__name__} is invalid"
        return error_message(message, 400)

    record = cls.query.get(id)

    if not record:
        message = f"{cls.__name__} {id} does not exist"
        return error_message(message, 404)
    return record

def validate_data(cls_method, request_body):
    try:
        data = cls_method(request_body)
    except KeyError:
        message = "Invalid data"
        return error_message(message, 400)
    return data    

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

def sort_records(cls, sort_query):
    sort_selection = ["asc", "desc"]
    
    if sort_query not in sort_selection:
        message = "Our sort selection is limited to: asc and desc"
        return error_message(message, 400)
    elif sort_query == "asc":
        records = cls.query.order_by(asc(cls.title))
    elif sort_query == "desc":
        records = cls.query.order_by(desc(cls.title))
    return records