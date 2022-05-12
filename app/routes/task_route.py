from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import asc, desc
from app import db
from app.models.task import Task
from sqlalchemy.sql.functions import now
import requests, os
from app.routes_helper import validated_task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({'details': "Invalid data"}, 400)
   
    new_task = Task.from_json(request_body)
    
    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_json()}, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = request.args

    if "sort" in task_query:
        if task_query["sort"] == "desc":
            tasks = Task.query.order_by(desc(Task.title)).all()
        else:
            tasks = Task.query.order_by(asc(Task.title)).all()
    else:
        # To get all the task from the table
         tasks = Task.query.all()

    tasks_response = [task.to_json() for task in tasks]

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validated_task(Task, task_id)

    return {"task": task.to_json()}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validated_task(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} \"{task.title}\" successfully deleted'}, 200

@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete_task(task_id):
    task = validated_task(Task, task_id)
    task.completed_at = now()

    db.session.add(task)
    db.session.commit()

    SLACK_API_URL = "https://slack.com/api/chat.postMessage"
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

    query_params = {
            "channel": "task_notifications",
            "text": f"Someone just completed the task {task.title}"
        }

    headers = {"Authorization": SLACK_BOT_TOKEN}

    url = requests.post(SLACK_API_URL, headers=headers, params=query_params)
    

    return {"task": task.to_json()}, 200

@tasks_bp.route('/<task_id>/mark_incomplete', methods=["PATCH"])
def mark_incomplete_task(task_id):
    task = validated_task(Task, task_id)
    task.completed_at = None

    db.session.add(task)
    db.session.commit()
    
    return {"task": task.to_json()}, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task_complete_date(task_id):
    task = validated_task(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.add(task)
    db.session.commit()

    return {"task": task.to_json()}, 200