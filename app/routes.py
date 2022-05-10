from re import A
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
from datetime import datetime
import requests
import os




task_list_bp = Blueprint("task_list", __name__, url_prefix='/tasks')

@task_list_bp.route('', methods = ['POST'])
def create_one_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response), 400))

    if "completed_at" in request_body:
        new_task = Task(title=request_body['title'], 
                    description=request_body['description'], completed_at=request_body['completed_at'])
    else:
        new_task = Task(title=request_body['title'], 
                    description=request_body['description'])

    # is_complete = check_is_completed(new_task)
    db.session.add(new_task)
    db.session.commit()
    # response = {
    #     "task":{
    #     "id": new_task.task_id,
    #     "title": new_task.title,
    #     "description":new_task.description,
    #     "is_complete": is_complete
    #     }
    # }
    response = make_task_response(new_task)
    return jsonify(response), 201


def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"msg":f"Invalid id: {task_id}"}
        abort(make_response(jsonify(response), 400))
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        #rsp = {"msg": f"Could not find task with id {task_id}"}
        response =  {"msg": "Task not found"}
        abort(make_response(jsonify(response), 404))
    return chosen_task

#helper function, checks if task is complete
def check_is_completed(task):
    if task.completed_at is None:
        is_complete = False
    else:
        is_complete = True
    
    return is_complete

#helper function, makes responses
def make_task_response(task):
    is_complete = check_is_completed(task)
    response = {
        "task": {
            'id': task.task_id,
            'title': task.title,
            'description': task.description,
            'is_complete': is_complete
        }
    }
    return response


@task_list_bp.route('/<task_id>', methods = ['GET'])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    #is_complete = check_is_completed(chosen_task)

    # rsp = {'task':{
    #     'id': chosen_task.task_id,
    #     'title': chosen_task.title,
    #     'description': chosen_task.description,
    #     'is_complete': is_complete
    # }}
    response = make_task_response(chosen_task)
    return jsonify(response), 200


@task_list_bp.route('', methods = ['GET'])
def get_all_tasks():

    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        is_complete = check_is_completed(task)

        tasks_response.append({
            'id': task.task_id,
            'title': task.title,
            'description': task.description,
            'is_complete': is_complete
        })

    #check params for sorting
    params = request.args
    sort_type = None
    if "sort" in params:
        if params["sort"] == "asc":
            #ascending
            sort_type = "A"
        else:
            #descending
            sort_type = "D"

    if sort_type == "A":
        tasks_response = (sorted(tasks_response, key=lambda i: i['title']))

    elif sort_type == "D":
        tasks_response = (sorted(tasks_response, key=lambda i: i['title'], reverse = True))
    
    return jsonify(tasks_response)

#SLACK API 
def message_slack(task):

    SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
    PATH = 'https://slack.com/api/chat.postMessage'
    query_params = {
        "channel":"task-notifications",
        "text":f"Someone just completed the task {task.title}"
    }
    header = {
        "Authorization" : f"Bearer {SLACK_TOKEN}"
    }

    response = requests.post(PATH, params=query_params, headers=header)


    return response




@task_list_bp.route('/<task_id>/mark_complete', methods = ['PATCH'])
def mark_complete(task_id):
    chosen_task = get_task_or_abort(task_id)

    #check if task was already completed, if not send message to slack
    if not check_is_completed(chosen_task):
        message_slack(chosen_task)


    chosen_task.completed_at = datetime.utcnow()
    
    #is_complete = check_is_completed(chosen_task)

    db.session.commit()

    # response = {
    #     "task": {
    #         'id': chosen_task.task_id,
    #         'title': chosen_task.title,
    #         'description': chosen_task.description,
    #         'is_complete': is_complete
    #     }
    # }
    response = make_task_response(chosen_task)

    return jsonify(response), 200

@task_list_bp.route('/<task_id>/mark_incomplete', methods = ['PATCH'])
def mark_incomplete(task_id):
    chosen_task = get_task_or_abort(task_id)
    chosen_task.completed_at = None
    #is_complete = check_is_completed(chosen_task)
    
    db.session.commit()

    response = make_task_response(chosen_task)

    # rsp = {
    #     "task": {
    #         'id': chosen_task.task_id,
    #         'title': chosen_task.title,
    #         'description': chosen_task.description,
    #         'is_complete': is_complete
    #     }
    # }
    return jsonify(response), 200


@task_list_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id):
    chosen_task = get_task_or_abort(task_id)

    request_body = request.get_json()
    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
        #completed_at
    except KeyError:
        return{
            "msg": "title and description are required"
        }, 400
    
    # is_complete = check_is_completed(chosen_task)

    db.session.commit()

    # rsp = {
    #     "task": {
    #     'id': chosen_task.task_id,
    #     'title': chosen_task.title,
    #     'description': chosen_task.description,
    #     'is_complete': is_complete
    #     }
    # }
    response = make_task_response(chosen_task)
    return jsonify(response), 200

@task_list_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id):

    chosen_task = get_task_or_abort(task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f"Task {chosen_task.task_id} \"{chosen_task.title}\" successfully deleted"
    }, 200



