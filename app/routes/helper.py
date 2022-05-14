import requests
import os


import requests
from os import CLD_STOPPED
from flask import abort, make_response
from app.models.task import Task
from app.models.goal import Goal

def validate_record(cls, id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"message": f"{cls} {id} is invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        return abort(make_response({"message": f"{cls.__name__} {id} not found"}, 404))

    return obj

def send_message_to_slack(task):
    path = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("SLACK_API")
    head = {"Authorization":API_KEY}

    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the '{task.title}' "
    }

    req = requests.post(path, headers=head,params=query_params)