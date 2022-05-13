import json
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
from sqlalchemy import desc
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    
    if "description" not in request_body.keys() or "title" not in request_body.keys():
        return make_response({"details": "Invalid data"}, 400) 

    
    else:
        new_task = Task(
            title=request_body["title"], 
            description=request_body["description"],
            completed_at=request_body["completed_at"] if "completed_at" in request_body else None)
        
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"task": {
                    "id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": bool(new_task.completed_at)
                }}), 201
    
# def get_model(id, Model):
#     if Model == Task:
#         model_type = "task"
#     elif Model == Goal:
#         model_type = "goal"
#     model = Model.query.get(id)
#     if not model:
#         abort(make_response({"error": f"{model_type} {id} not found"}, 404))
#     return model
    
def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid.  Must be numerical"}, 400))
        
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))
        
    return task

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    sorting_query = request.args.get("sort")
    
    if sorting_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    elif sorting_query == "asc":
        tasks = Task.query.order_by(Task.title)
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })
    return jsonify(tasks_response)
            


@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = validate_task_id(task_id)
    rsp = { 'task': {
        'id': chosen_task.task_id,
        'title': chosen_task.title,
        'description': chosen_task.description,
        'is_complete': bool(chosen_task.completed_at)
    }}

    return jsonify(rsp), 200


@tasks_bp.route('/<task_id>', methods=['PUT'])
def put_one_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        return jsonify(rsp), 400
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        rsp = {"msg": "Task not found"}
        return jsonify(rsp), 404

    request_body = request.get_json()
    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
        
    except KeyError:
        return {
            "msg": "Title and description are required"
        }, 400
    db.session.commit()

    return make_response({"task": { "id": chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": bool(chosen_task.completed_at) 
                }})

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        return jsonify(rsp), 400
    
    chosen_task = Task.query.get(task_id)
    if chosen_task is None:
        rsp = {'message': f'Task {task_id} not found'}
        return jsonify(rsp), 404

    db.session.delete(chosen_task)
    db.session.commit()

    return make_response({"details": f"Task {chosen_task.task_id} \"{chosen_task.title}\" successfully deleted"}) 


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task_id(task_id)
    task.completed_at = None
    db.session.commit()
    
    response_body = {"task" : task.get_dict()}
    return jsonify(response_body), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task_id(task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    
    SLACK_URL = 'https://slack.com/api/chat/postMessage'
    post_msg = {"text": f"Someone just completed the task {task.title}", "channel" : "C03FABVBLS0"}
    auth = os.environ.get('SLACK_BOT_TOKEN')
    requests.post(SLACK_URL, json=post_msg, headers={'Authorization' : f'Bearer {auth}'})
    rsp = {"task" : task.get_dict()}
    return jsonify(rsp), 200
    