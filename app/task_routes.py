
from flask import Blueprint, request
from app import db
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

    return success_message(dict(task=new_task.self_to_dict_no_goal()), 201)


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_param = request.args.get("sort")
    tasks = Task.query.all()
    all_tasks = [task.self_to_dict_no_goal() for task in tasks]

    if not sort_param:
        return return_database_info_list(all_tasks)
    if sort_param == "asc":
        sorted_tasks_asc = sorted(all_tasks, key = lambda i : i["title"])
        return return_database_info_list(sorted_tasks_asc)
    if sort_param == "desc":
        sorted_tasks_desc = sorted(all_tasks, key = lambda i : i["title"], reverse=True)
        return return_database_info_list(sorted_tasks_desc)


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_record_by_id(Task, task_id)

    if task.goal_id:
        return return_database_info_dict("task", task.self_to_dict_with_goal())
    else:
        return return_database_info_dict("task", task.self_to_dict_no_goal())


@task_bp.route("/<task_id>", methods=["PUT", "PATCH"])
def update_task_by_id(task_id):
    task = get_record_by_id(Task, task_id)

    request_body = request.get_json()
    update_record_safely(Task, task, request_body)

    db.session.commit()

    return return_database_info_dict("task", task.self_to_dict_no_goal())


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

    return return_database_info_dict("task", task.self_to_dict_no_goal())


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_record_by_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return success_message(dict(details=f'Task {task.task_id} "{task.title}" successfully deleted'))