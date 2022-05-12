
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

# Sorting helper functions

def sort_tasks(all_tasks, sort_param):
    if sort_param != "asc" and sort_param != "desc":
        return error_message(f"Invalid sort parameter '{sort_param}'. Sort parameter may only be 'asc' or 'desc'.", 400)
    elif sort_param == "asc":
        sorted_tasks_asc = sorted(all_tasks, key = lambda i : i["title"])
        return sorted_tasks_asc
    elif sort_param == "desc":
        sorted_tasks_desc = sorted(all_tasks, key = lambda i : i["title"], reverse=True)
        return sorted_tasks_desc

def filter_tasks_by_title(all_tasks, title_filter):
    filtered_tasks = [task for task in all_tasks if title_filter.lower() in task["title"].lower()]
    if filtered_tasks:
            return filtered_tasks
    else:
        return error_message(f"Search parameter '{title_filter}' not found in any tasks.", 404)

def filter_tasks_by_description(all_tasks, description_filter):
    filtered_tasks = [task for task in all_tasks if description_filter.lower() in task["description"].lower()]
    if filtered_tasks:
            return filtered_tasks
    else:
        return error_message(f"Search parameter '{description_filter}' not found in any tasks.", 404)
    

def filter_tasks_by_title_and_description(all_tasks, title_filter, description_filter):
    # didn't do a list comprehension for this one because there's so much going on it felt too difficult to read
    filtered_tasks = []
    for task in all_tasks:
        if title_filter.lower() in task["title"].lower() and description_filter.lower() in task["description"].lower():
            filtered_tasks.append(task)
    if filtered_tasks:
            return filtered_tasks
    else:
        return error_message(f"Search parameter(s) '{title_filter}' and/or '{description_filter}' not found in any tasks.", 404)



@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    all_tasks = [task.self_to_dict_no_goal() for task in tasks]
    sort_param = request.args.get("sort")
    description_param = request.args.get("description")
    title_param = request.args.get("title")

    # if no parameters
    if not sort_param and not title_param and not description_param:
        return return_database_info_list(all_tasks)

    # if sort param only
    elif sort_param and not description_param and not title_param:
        sorted_tasks = sort_tasks(all_tasks, sort_param)
        return return_database_info_list(sorted_tasks)

    # if description param only
    elif description_param and not sort_param and not title_param:
        filtered_tasks = filter_tasks_by_description(all_tasks, description_param)
        return return_database_info_list(filtered_tasks)

    # if title param only
    elif title_param and not sort_param and not description_param:
        filtered_tasks = filter_tasks_by_title(all_tasks, title_param)
        return return_database_info_list(filtered_tasks)
    
    # if title and description param only
    elif title_param and description_param and not sort_param:
        double_filtered_tasks = filter_tasks_by_title_and_description(all_tasks, title_param, description_param)
        return return_database_info_list(double_filtered_tasks)

    # if sort and description param only
    elif sort_param and description_param and not title_param:
        filtered_tasks = filter_tasks_by_description(all_tasks, description_param)
        sorted_tasks = sort_tasks(filtered_tasks, sort_param)
        return return_database_info_list(sorted_tasks)
    
    # if sort and title param only
    elif sort_param and title_param and not description_param:
        filtered_tasks = filter_tasks_by_title(all_tasks, title_param)
        sorted_tasks = sort_tasks(filtered_tasks, sort_param)
        return return_database_info_list(sorted_tasks)
    
    # if all parameters
    elif sort_param and title_param and description_param:
        double_filtered_tasks = filter_tasks_by_title_and_description(all_tasks, title_param, description_param)
        sorted_tasks = sort_tasks(double_filtered_tasks, sort_param)
        return return_database_info_list(sorted_tasks)
    

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