import os
import requests
from datetime import datetime
from flask import jsonify, request, abort, make_response
from app.models.task import Task
from app.models.goal import Goal

def validate_id(model, id):
    try:
        id = int(id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_obj = model.query.get(id)
    if chosen_obj is None:
        rsp = {"msg": f"Could not find id {id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_obj

# Validate there are title and description when creating or updating task
def validate_task_attributes(request_body):
    try:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body.get("completed_at"))
        return new_task
    except:
        rsp = {
            "details": "Invalid data"
        }
        abort(make_response(jsonify(rsp), 400))


# Validate there is title when creating or updating a goal
def validate_goal_attributes(request_body):
    try:
        new_goal = Goal(title=request_body["title"])
        return new_goal
    except:
        rsp = {
            "details": "Invalid data"
        }
        abort(make_response(jsonify(rsp), 400))
    

def call_Slack_API(task):
    SLACKBOT_TOKEN = os.environ.get("SLACKBOT_TOKEN")
    slackbot_url = "https://slack.com/api/chat.postMessage"
    slackbot_headers =  {"Authorization": f"Bearer {SLACKBOT_TOKEN}"}
    slackbot_msg = {
            "channel": "task-notifications", 
            "text": f"Someone just completed the task {task.title}"
    }
    requests.post(slackbot_url, data=slackbot_msg, headers=slackbot_headers)

# test not working
# def validate_datetime(date_time):
#     if date_time is None:
#         return None

#     try:
#         return datetime.strptime(date_time, '%a, %d %b %Y %H:%M:%S %Z')
#     except ValueError:
#         rsp = {
#             "msg": f"Invalid value of completed_at: {date_time}"
#         }
#         abort(make_response(jsonify(rsp), 400))