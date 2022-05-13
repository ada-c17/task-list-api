from app.models.task import Task
from app.models.goal import Goal
from flask import jsonify, abort, make_response
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# def fetch_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response(jsonify({"details":f"invalid data"}), 400))

#     task = Task.query.get(task_id)

#     if not task:
#         abort(make_response(jsonify({"details": f"task {task_id} not found"}), 404))
#     return task

# def fetch_goal(goal_id):
#     try:
#         goal_id = int(goal_id)
#     except:
#         abort(make_response(jsonify({"details":f"invalid data"}), 400))

#     goal = Goal.query.get(goal_id)

#     if not goal:
#         abort(make_response(jsonify({"details": f"goal {goal_id} not found"}), 404))
#     return goal

def fetch_type(type, id):
    try:
        id = int(id)
    except:
        abort(make_response(jsonify({"details":f"invalid data"}), 400))

    if type == "goal":
        got_type = Goal.query.get(id)
    elif type == "task":
        got_type = Task.query.get(id)

    if not got_type:
        abort(make_response(jsonify({"details": f"{type} {id} not found"}), 404))
    return got_type

def slack_post(name):
    
    url_location = "https://slack.com/api/chat.postMessage"
    data_dict = {"channel": "C03ERAGUTR8", 
                "text": f"Someone just completed the task {name}"}
    auth_info = os.environ.get("SLACKBOT_TOKEN")
    slack_response = requests.request("POST", url_location, data=data_dict, headers={"Authorization": auth_info})
    
    