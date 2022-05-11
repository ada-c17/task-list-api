'''
ROUTES
-------------------------
Defines endpoints for *tasks* and *goals* for the Task List API.

TABLE OF CONTENTS:
    [0] Imports
    [1] Helper Functions
    [2] Blueprints
    [3] *TASK* endpoints
    [4] *GOAL* endpoints
'''



##### IMPORTS #################################################################

from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
import datetime
import requests
import os




##### HELPER FUNCTIONS ########################################################

def validate_object(object_id, object_type):
    '''
    Validates the goal or task based on ID and fetches the object from the database.
        *object_id:  id of a task or goal
        *object_type: "goal" or "task" depending on endpoint
        OUTPUT: goal or task object fetched from database.
    '''
    try:
        object_id = int(object_id)
    except:
        abort(make_response({"message":f"Object {object_id} invalid"}, 400))

    if object_type == "task":
        goal_or_task = Task.query.get(object_id)
    elif object_type == "goal":
        goal_or_task = Goal.query.get(object_id)
    if not goal_or_task:
        abort(make_response({"message":f"Object {object_id} not found"}, 404))

    return goal_or_task

def post_to_slack(title):
    '''
    This function posts a completion method to slack with a slackbot when the
    patch command "complete_task" is run.
        *title: title of the task or goal (e.g. task.title)
        OUTPUT: None (run in place)
    '''
    PATH = "https://api.slack.com/api/chat.postMessage"
    SLACK_AUTH_TOKEN = os.environ.get("SLACK_TOKEN")

    query_params = {
        "channel":"task-list",
        "text":f'Someone just completed the task {title}'
    }
    header = {"Authorization":SLACK_AUTH_TOKEN}
    requests.post(PATH, params=query_params, headers=header)

def ordered_tasks_query(sort_method):
    '''
    Determines the order_by type (if any) for GET all tasks when called.
        *sort_method: Evaluates to "asc" or "desc".
            ALWAYS pass in request.args.get("sort") when calling
        OUTPUT: returns the ordered tasks.
    '''
    if sort_method == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_method == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    return tasks

def validate_task_request_body(request_body):
    if "title" in request_body and "description" in request_body:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
    else:
        abort(make_response({"details": "Invalid data"}, 400))
    return task



##### BLUEPRINTS ##############################################################

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")




##### TASK ENDPOINTS ##########################################################

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = ordered_tasks_query(request.args.get("sort"))
    return jsonify([task.to_dict() for task in tasks])


@tasks_bp.route("", methods=["POST"])
def post_task():
    request_body = request.get_json()
    if "title" in request_body and "description" in request_body:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_object(task_id, "task")
    return jsonify({"task":task.to_dict()})


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_object(task_id, "task")

    request_body = request.get_json()

    if "title" in request_body and "description" in request_body:
        task.title = request_body["title"]
        task.description = request_body["description"]
        if "completed_at" in request_body:
            task.completed_at = request_body["completed_at"]
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.commit()

    return make_response({"task":task.to_dict()})


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_object(task_id, "task")

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = validate_object(task_id, "task")
    request_body = request.get_json()

    task.completed_at = datetime.datetime.utcnow()
    db.session.commit()

    post_to_slack(task.title)

    return make_response({"task":task.to_dict()})


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    task = validate_object(task_id, "task")
    request_body = request.get_json()

    task.completed_at = None
    db.session.commit()

    return make_response({"task":task.to_dict()})




##### GOAL ENDPOINTS ##########################################################










