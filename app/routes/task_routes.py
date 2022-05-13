import os
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request
from datetime import datetime
from app.routes.helper import validate_id, validate_task_attributes, call_Slack_API

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    new_task = validate_task_attributes(request_body)

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

    rsp = [task.to_dict() for task in tasks]
    
    return jsonify(rsp), 200

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = validate_id(Task, task_id)

    rsp = {"task": chosen_task.to_dict()}
    return jsonify(rsp), 200

@tasks_bp.route("/<task_id>", methods=['PUT'])
def put_one_task(task_id):
    chosen_task = validate_id(Task, task_id)
    new_task = validate_task_attributes(request.get_json())

    chosen_task.title = new_task.title
    chosen_task.description = new_task.description
    
    db.session.commit()    
    
    rsp = {"task": chosen_task.to_dict()} #refactor? can i remove "task"
    return jsonify(rsp), 200

@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_one_task(task_id):
    chosen_task = validate_id(Task, task_id)

    db.session.delete(chosen_task)
    db.session.commit()
    rsp = {
        "details": f'Task {task_id} "{chosen_task.title}" successfully deleted'
    }
    return jsonify(rsp), 200

# ------------- WAVE 3 -------------
@tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def update_task_mark_incomplete(task_id):
    chosen_task = validate_id(Task, task_id)
    
    chosen_task.completed_at = None

    db.session.commit()

    rsp = {"task": chosen_task.to_dict()}

    return jsonify(rsp), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def update_task_mark_complete(task_id):
    chosen_task = validate_id(Task, task_id)
    
    chosen_task.completed_at = datetime.now() 

    # WAVE 4
    call_Slack_API(chosen_task)

    db.session.commit()

    rsp = {"task": chosen_task.to_dict()}

    return jsonify(rsp), 200