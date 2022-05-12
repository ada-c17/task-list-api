from flask import Blueprint,jsonify, request, make_response, abort
from app.models.task import Task
from app import db
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("task", __name__,url_prefix="/tasks")

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400
    new_task = Task(title=request_body["title"],
                  description=request_body["description"])

    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task":{
        "id":new_task.task_id,
        "title":new_task.title,
        "description": new_task.description,
        "is_complete": bool(new_task.completed_at) }
    }
    return jsonify(response), 201

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))

    else:
        tasks= Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append({
            'id':task.task_id,
            'title':task.title,
            'description':task.description,
            'is_complete': bool(task.completed_at)
        })
    return jsonify(task_response),200


def get_task_or_abort(task_id):
    try:
        task_id = int (task_id)
    except ValueError:
        rsp =  {"msg": f"Invalid id:{task_id}"}
        abort( make_response (jsonify(rsp), 400))
        
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        abort( make_response({"massage": f" task {task_id} not found"}, 404))
    
    return chosen_task

# get one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    request_body = request.get_json()
    rsp = {
        "task":{
        'id':chosen_task.task_id,
        'title':chosen_task.title,
        'description':chosen_task.description,
        'is_complete':bool(chosen_task.completed_at)}
    }
    if chosen_task.goal_id:
        rsp["task"]["goal_id"] = chosen_task.goal_id  

    return jsonify(rsp), 200

# update chosen task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    request_body = request.get_json()

    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]

    except KeyError:
        return {
            "msg": "title, and description are required"
        },404

    db.session.commit()

    rsp = {
        "task":{
        'id':chosen_task.task_id,
        'title':chosen_task.title,
        'description':chosen_task.description,
        'is_complete':bool(chosen_task.completed_at)}
    }

    return jsonify(rsp), 200


# delete chosen task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    response_body = { 
        "details":f'Task {chosen_task.task_id} "{chosen_task.title}" successfully deleted'
    }

    return jsonify(response_body), 200

# update chosen task is completed
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_is_complete(task_id):
    chosen_task = get_task_or_abort(task_id)

    chosen_task.completed_at = datetime.utcnow()
    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
    data={
        "channel": "task-notifications",
        "text": f"{chosen_task.title} is completed",
        "format":"json"
    }

    headers = { "Authorization": f"Bearer { SLACK_TOKEN }"
    }

    requests.post(path, params=data, headers=headers )


    rsp = {
        "task":{
        'id':chosen_task.task_id,
        'title':chosen_task.title,
        'description':chosen_task.description,
        'is_complete':bool(chosen_task.completed_at)}
    }

    return jsonify(rsp), 200

# update chosen task is Incompleted
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_is_incomplete(task_id):
    chosen_task = get_task_or_abort(task_id)

    chosen_task.completed_at = None

    db.session.commit()

    rsp = {
        "task":{
        'id':chosen_task.task_id,
        'title':chosen_task.title,
        'description':chosen_task.description,
        'is_complete':bool(chosen_task.completed_at)}
    }

    return jsonify(rsp), 200


