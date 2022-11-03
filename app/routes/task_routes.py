from sqlalchemy import true
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime
from tests.test_wave_01 import test_create_task_must_contain_description
from .routes_helper import error_message, make_task_safely, get_task_record_by_id, replace_task_safely

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#POST /tasks
@bp.route("", methods=("POST",))
def create_task():
    request_body = request.get_json()
    
    task=make_task_safely(request_body)

    db.session.add(task)
    db.session.commit()
    result={"task":(task.to_dict())}
    return jsonify(result), 201

#GET /tasks
@bp.route("",methods=["GET"])
def get_tasks():
    title_param = request.args.get("sort")

    if title_param == 'asc':
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif title_param == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
        
    result_list = [task.to_dict() for task in tasks]

    return (jsonify(result_list))

# GET /tasks/<task_id>
@bp.route("/<task_id>",methods=["GET"])
def get_task_by_id(task_id):
    task = get_task_record_by_id(task_id)
    result={"task":(task.to_dict())}
    return jsonify(result)

#PUT /tasks/<task_id>
@bp.route("/<task_id>",methods=["PUT"])
def replace_task_by_id(task_id):
    request_body = request.get_json()
    task = get_task_record_by_id(task_id)

    replace_task_safely(task, request_body)

    db.session.commit()
    result={"task":(task.to_dict())}
    return jsonify(result)

#DELETE /tasks/<task_id>
@bp.route("/<task_id>",methods=["DELETE"])
def delete_task_by_id(task_id):
    task = get_task_record_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    result={"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}
    return make_response(jsonify(result), 200)

#PATCH /tasks/<task_id>
@bp.route("/<task_id>",methods=["PATCH"])
def update_task_by_id(task_id):
    task = get_task_record_by_id(task_id)
    request_body = request.get_json()
    task_keys = request_body.keys()

    if "title" in task_keys:
        task.title = request_body["title"]
    if "description" in task_keys:
        task.description = request_body["description"]
    
    db.session.commit()
    return jsonify(task.to_dict)

#PATCH /tasks/<task_id>/mark_complete
@bp.route("/<task_id>/mark_complete",methods=["PATCH"])
def update_mark_as_complete_by_id(task_id):
    task = get_task_record_by_id(task_id)
    request_body = request.get_json()
    
    task.completed_at = datetime.utcnow()

    db.session.commit()
    result={"task":(task.to_dict())}
    return jsonify(result)

#PATCH /tasks/<task_id>/mark_incomplete
@bp.route("/<task_id>/mark_incomplete",methods=["PATCH"])
def update_mark_as_incomplete_by_id(task_id):
    task = get_task_record_by_id(task_id)
    request_body = request.get_json()
    
    task.completed_at = None

    db.session.commit()
    result={"task":(task.to_dict())}
    return jsonify(result)
