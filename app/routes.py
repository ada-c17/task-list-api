import os
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request, abort, make_response
from datetime import datetime
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# Validate there are title and description when creating or updating task
def validate_create_or_put():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body.get("completed_at"))
    except:
        rsp = {
            "details": "Invalid data"
        }
        abort(make_response(jsonify(rsp), 400))
    
    return new_task

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    new_task = validate_create_or_put()
    
    db.session.add(new_task)
    db.session.commit()
    return {"task": new_task.to_dict()}, 201
    
@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    sort_params = request.args.get("sort")

    if sort_params == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_params == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    rsp = []
    
    for task in tasks:
        rsp.append(task.to_dict())

    return jsonify(rsp), 200

def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_task = Task.query.get(task_id)
    if chosen_task is None:
        rsp = {"msg": f"Could not find task with id {task_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_task

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    rsp = {"task": chosen_task.to_dict()}
    return jsonify(rsp), 200

@tasks_bp.route("/<task_id>", methods=['PUT'])
def put_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    new_task = validate_create_or_put()

    chosen_task.title = new_task.title
    chosen_task.description = new_task.description
    
    db.session.commit()    
    
    rsp = {"task": chosen_task.to_dict()}
    return jsonify(rsp), 200

@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    db.session.delete(chosen_task)
    db.session.commit()
    rsp = {
        "details": f'Task {task_id} "{chosen_task.title}" successfully deleted'
    }
    return jsonify(rsp), 200

# ------------- WAVE 3 -------------
@tasks_bp.route("/<task_id>/<complete_status>", methods=['PATCH'])
def update_task_complete_status(task_id, complete_status):
    chosen_task = get_task_or_abort(task_id)
    
    if "mark_incomplete" in complete_status:
        chosen_task.completed_at = None
    elif "mark_complete" in complete_status:
        chosen_task.completed_at = datetime.now() 

        # WAVE 4
        SLACKBOT_TOKEN = os.environ.get("SLACKBOT_TOKEN")
        slackbot_url = "https://slack.com/api/chat.postMessage"
        slackbot_headers =  {"Authorization": "Bearer " + SLACKBOT_TOKEN}
        slackbot_msg = {
                "channel": "task-notifications", 
                "text": f"Someone just completed the task {chosen_task.title}"
        }
        requests.post(slackbot_url, data=slackbot_msg, headers=slackbot_headers)

    db.session.commit()

    rsp = {"task": chosen_task.to_dict()}

    return jsonify(rsp), 200