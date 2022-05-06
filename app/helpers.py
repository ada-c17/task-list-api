from flask import abort, make_response
from app.models.task import Task
import requests
from dotenv import load_dotenv
import os


def validate(task_id):
    try:
        task_id = int(task_id)
    except:
        return abort(make_response({"message": f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        return abort(make_response({"message": f"task {task_id} not found"}, 404))
    return task


def call_slack(msg):
    PATH = "https://slack.com/api/chat.postMessage"

    query_params = {
        "channel": "task-notifications",
        "text": msg,
        "charset": "utf-8"
    }

    header = {
        "Authorization": "Bearer " + os.environ.get("SLACK_TOKEN")
    }

    requests.post(PATH, params=query_params, headers=header)
