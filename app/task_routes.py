
from flask import Blueprint, request
from app import db
from sqlalchemy import asc, desc
from app.models.task import Task
from app.helper_functions import *
import datetime as dt
from datetime import date


task_bp = Blueprint("Tasks", __name__, url_prefix="/tasks")


# Route functions


@task_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    new_task = create_record_safely(Task, request_body)

    db.session.add(new_task)
    db.session.commit()

    return success_message_info_as_list(dict(task=new_task.self_to_dict()), 201)


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_param = request.args.get("sort")
    description_param = request.args.get("description")
    title_param = request.args.get("title")
    query = Task.query

    if title_param:
        query = query.filter(Task.title.ilike(f"%{title_param}%"))
        if not query.all():
            return error_message(f"Search parameter '{title_param}' not found in any tasks.", 404)
    if description_param:
        query = query.filter(Task.description.ilike(f"%{description_param}%"))
        if not query.all():
            return error_message(f"Search parameter '{description_param}' not found in any tasks.", 404)
    if sort_param:
        if sort_param == "asc":
            query = query.order_by(asc(Task.title))
        elif sort_param == "desc":
            query = query.order_by(desc(Task.title))
        else:
            return error_message(f"Invalid sort parameter '{sort_param}'. Sort parameter may only be 'asc' or 'desc'.", 400)
    
    tasks = query.all()
    all_tasks = [task.self_to_dict() for task in tasks]
    
    return success_message_info_as_list(all_tasks)


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_record_by_id(Task, task_id)

    return return_database_info_dict("task", task.self_to_dict())


@task_bp.route("/<task_id>", methods=["PUT", "PATCH"])
def update_task_by_id(task_id):
    task = get_record_by_id(Task, task_id)

    request_body = request.get_json()
    update_record_safely(Task, task, request_body)

    db.session.commit()

    return return_database_info_dict("task", task.self_to_dict())


@task_bp.route("/<task_id>/<completion_status>", methods=["PATCH"])
def update_task_completion_status(task_id, completion_status):
    task = get_record_by_id(Task, task_id)

    if completion_status == "mark_complete":
        completion_info = {
            "completed_at" : dt.date.today()
        }
        update_record_safely(Task, task, completion_info)
        send_slackbot_message(task.title)
        
    elif completion_status == "mark_incomplete":
        completion_info = {
            "completed_at" : None
        }
        update_record_safely(Task, task, completion_info)

    db.session.commit()

    return return_database_info_dict("task", task.self_to_dict())


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_record_by_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return success_message_info_as_list(dict(details=f'Task {task.task_id} "{task.title}" successfully deleted'))