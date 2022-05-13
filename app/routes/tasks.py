import requests
#from requests_oauthlib import OAuth1
import os
from dotenv import load_dotenv
from app import db
from flask import Blueprint, jsonify, make_response, request
from datetime import datetime, timezone
from app.models.task import Task
from app.models.goal import Goal
from app.routes.request_helpers import handle_id_request, check_complete_request_body

load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def slack_complete(task):
    url = "https://slack.com/api/chat.postMessage"
    slack_message = f"{task.title} was completed! \U0001F4AF"

    query_params = {
        "channel": "task-completion",
        "text": slack_message
    }
    auth_token = os.environ.get("SLACKBOT_API_TOKEN")
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(url, params=query_params, headers=headers)
    return response

def slack_goal_complete(task):
    url = "https://slack.com/api/chat.postMessage"
    goal = task.goal
    slack_message = f"Goal achieved!\U0001F389 All tasks for '{goal.title}' were completed."

    query_params = {
        "channel": "task-completion",
        "text": slack_message
    }
    auth_token = os.environ.get("SLACKBOT_API_TOKEN")
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(url, params=query_params, headers=headers)
    return response

def last_task_in_goal(task):
    task_goal = task.goal
    task_list = task_goal.tasks
    if all(task.completed_at for task in task_list):
        return True
    else:
        return False

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    query_params = request.args.to_dict(flat=False)
    #note that if multiple inputs for one param (e.g. sort=asc&sort=desc),
    #to_dict will restrict to first input ({"sort":"asc"})
    #in this case, if subsequent inputs are invalid, no warning will be sent
    #with response
    if "title" in query_params:
        #title search is case-insensitive and inclusive
        #i.e. if title=task is passed in, tasks with "task", "TASK", "Task" etc
        # in the title will be returned
        titles = query_params["title"]
        inclusive_title = f"%{titles[0]}%"
        task_list = Task.query.filter(Task.title.ilike(inclusive_title))
        if len(titles) > 1:
            for title in titles[1:]:
                inclusive_title = f"%{title}%"
                task_list = task_list.query.filter(Task.title.ilike(inclusive_title))
        query_params.pop("title")

    #currently must choose one; sort for title-based search unimplemented
    #and title search preferred over sorting
    elif "sort" in query_params:
        #to limit time here, could put restriction on length of sorts
        sorts = query_params["sort"]
        #in the case of conflicting inputs (e.g. sort=asc&sort=desc)
        #prefers asc. asc, desc defaults to title with no input but
        #will do id if id specified
        if "asc" in sorts:
            if "id" in sorts:
                task_list = Task.query.order_by(Task.task_id.asc()).all()
                sorts.remove("id")
            else:
                task_list = Task.query.order_by(Task.title.asc()).all()
            sorts.remove("asc")
        elif "desc" in sorts:
            if "id" in sorts:
                task_list = Task.query.order_by(Task.task_id.desc()).all()
                sorts.remove("id")
            else:
                task_list = Task.query.order_by(Task.title.desc()).all()
            sorts.remove("desc")
        elif "id" in sorts:
            #defaults to ascending order
            task_list = Task.query.order_by(Task.task_id).all()
            sorts.remove("id")
        else: 
            task_list = Task.query.all()
        if not sorts:
            query_params.pop("sort")

    else: 
        task_list = Task.query.all()

    task_response = []

    for task in task_list:
        task_response.append(task.make_response_dict())
    
    if query_params:
        #this warning affects the structure of the returned json
        #without: an array of json objects representing tasks
        #with: an array where array[0] is a json object of the warning
        #and array[1] is the array of json objects representing tasks
        #I think this should be fine since throwing an index error 
        #in the user's code would cue the user to look at the json 
        #and then see the warning
        warning = {
            "warning": "Unexpected query parameters in request.",
            "unused_params": query_params
            }
        task_response = jsonify(warning, task_response)
    else:
        task_response = jsonify(task_response)

    return make_response(task_response, 200)


@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = check_complete_request_body(request, Task)
    new_task = Task().create_from_request(request_body)

    db.session.add(new_task)
    db.session.commit()

    confirmation_msg = {"task": new_task.make_response_dict()}
    if "completed_at" in request_body and new_task.completed_at == None:
        confirmation_msg["warning"] = "Invalid completed_at. Valid formats: datetime.utcnow(), yyyy-mm-dd hh:mm:ss, yyyy-mm-dd hh:mm. Update with PUT task/<id> or POST task/<id>/mark-complete."

    return make_response(jsonify(confirmation_msg), 201)

@tasks_bp.route("/<id>", methods=["GET"])
def get_task_by_id(id):
    task = handle_id_request(id, Task)
    confirmation_msg = {"task": task.make_response_dict()}
    return make_response(jsonify(confirmation_msg), 200)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task_by_id(id):
    request_body = check_complete_request_body(request, Task)
    task_to_update = handle_id_request(id, Task)

    task_to_update.create_from_request(request_body)

    db.session.commit()

    return make_response(
        jsonify({"task": task_to_update.make_response_dict()}),
        200
        )


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task_by_id(id):
    task = handle_id_request(id, Task)
    db.session.delete(task)
    db.session.commit()

    return make_response(
            jsonify({"details": f"Task {id} \"{task.title}\" successfully deleted"}), 
            200
            )

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task = handle_id_request(id, Task)
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    confirmation_msg = {"task": task.make_response_dict()}

    slack_complete(task)

    if task.goal:
        if last_task_in_goal(task):
            slack_goal_complete(task)


    #slack_response = slack_complete(task)
    #confirmation_msg["slack-response"] = slack_response.json()
    #for troubleshooting response from Slack API through postman
    return make_response(jsonify(confirmation_msg), 200)

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task = handle_id_request(id, Task)
    task.completed_at = None
    db.session.commit()

    confirmation_msg = {"task": task.make_response_dict()}

    return make_response(jsonify(confirmation_msg), 200)