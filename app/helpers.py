from flask import abort, make_response
from app.models.task import Task
from app.models.goal import Goal
import requests
import os


def validate(id, model, name):
    try:
        id = int(id)
    except:
        return abort(make_response({"message": f"{name} {id} invalid"}, 400))

    record = model.query.get(id)
    if not record:
        return abort(make_response({"message": f"{name} {id} not found"}, 404))
    return record


# def validate_goal(goal_id):
#     try:
#         goal_id = int(goal_id)
#     except:
#         return abort(make_response({"message": f"goal {goal_id} invalid"}, 400))

#     goal = Goal.query.get(goal_id)
#     if not goal:
#         return abort(make_response({"message": f"goal {goal_id} not found"}, 404))
#     return goal


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
