from flask import Blueprint, jsonify, request, make_response, abort, Flask
from app.models.task import Task
from app.models.goal import Goal
import os
import requests

def validate_task(cls, id):
    try:
        task_id = int(id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    obj = cls.query.get(id)

    if not obj:
        abort(make_response({"message": f"{cls.__name__} not found"}, 404))

    return obj
def get_sorted_obj(cls):
    sorting_query = request.args.get('sort')
    if sorting_query == "asc":
        obj = cls.query.order_by(cls.title).all()
    elif sorting_query == "desc":
        obj = cls.query.order_by(cls.title.desc()).all()
    else:
        obj = cls.query.all()
    return obj

def call_slack(response_message):
    
    path = "https://slack.com/api/chat.postMessage"

    #Headers = {"Authorization": os.environ.get("SLACK_TOKEN")}
    Headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"
    }
    query_params = {
        "channel": "task-notifications",
        "text": response_message
    }
    response = requests.post(path, params=query_params, headers=Headers)
    return response.json()
