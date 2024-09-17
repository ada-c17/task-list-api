from email import header
from app import db
from flask import Blueprint, request,make_response, abort,jsonify
from app.models.task import Task
from app.models.goal import Goal
import requests
from datetime import datetime
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#Helper Function:
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"details": "Not found"}, 404))
    return task


@tasks_bp.route("", methods = ["POST"])
def post_new_task():

    new_task = Task.task_from_JSON()

    db.session.add(new_task)
    db.session.commit()

    return (make_response(new_task.task_to_JSON(), 201))

@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():

    params = request.args
    if params:
        if params.get("sort") == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif params.get("sort") == "desc":
            tasks= Task.query.order_by(Task.title.desc()).all()
        elif params.get("sort") == "id":
            tasks= Task.query.order_by(Task.task_id)
        elif "title" in params:
            tasks = Task.query.filter_by(title = params["title"]).all()
    else:
        tasks = Task.query.all()

    tasks_response = [task.task_to_JSON()["task"] for task in tasks]

    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):

    chosen_task = validate_task(task_id)

    return (make_response(chosen_task.task_to_JSON(), 200))

@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_one_task(task_id):

    updating_task = validate_task(task_id)

    updating_task.title = Task.task_from_JSON().title
    updating_task.description = Task.task_from_JSON().description
    updating_task.completed_at = Task.task_from_JSON().completed_at

    db.session.commit()

    return updating_task.task_to_JSON()

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):

    chosen_task = validate_task(task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    return (make_response({"details":f"Task {task_id} \"{chosen_task.title}\" successfully deleted"}), 200)


@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def patch_mark_complete(task_id):

    chosen_task = validate_task(task_id)

    chosen_task.completed_at = datetime.utcnow()

    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"

    query_params ={
        "channel": "task-notification",
        "text": f"Someone just completed the task {chosen_task.title}"
    }
    header = {"Authorization": os.environ.get(
            "SLACK_API_TOKEN")}

    response = requests.post(path, params = query_params, headers= header)
    
    return chosen_task.task_to_JSON()

@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def patch_mark_incomplete(task_id):

    chosen_task = validate_task(task_id)

    chosen_task.completed_at = None

    db.session.commit()
    
    return chosen_task.task_to_JSON()
