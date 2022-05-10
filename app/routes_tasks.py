import datetime
from flask import Blueprint, jsonify, request, abort, make_response
from .models.task import Task
from app import db
import os
import requests

task_bp = Blueprint("task_bp",__name__, url_prefix="/tasks" )

# Helper Functions:
def complete_or_not(task):
    '''
    Converts 'completed_at' task attribute to Boolean for 'is_completed' variable in response body
    '''
    if task.completed_at is not None:
        return True
    else:
        return False

def validate_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    return task

    
# Create: POST requests
# Sample request body: {"title": "A Brand New Task", "description": "Test Description"}
@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    try: 
        if 'completed_at' in request_body: # alternate: if request_body.get('completed_at')  # Dictionary method to get value of attribute; or return None
            new_task = Task(title=request_body['title'], description=request_body['description'], completed_at=request_body['completed_at'])
        else:
            new_task = Task(title=request_body['title'], description=request_body['description'])
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    is_complete = complete_or_not(new_task) # use of helper function to obtain T/F
    db.session.add(new_task)
    db.session.commit()

    response =  {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
        } 
        }
    return jsonify(response), 201


# Read: GET
# Endpoint with params: "/tasks?sort=asc" and "/tasks?sort=desc"
#Params: key:sort with values: asc, desc

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        is_complete = complete_or_not(task)
        task_list.append( 
        {   "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete})

    def get_title(task_list):            # https://www.programiz.com/python-programming/methods/list/sort
        return task_list.get('title')
    
    param_value = request.args.get('sort')    # query_param_value = request.args.get(query_param_key)
    if param_value == 'asc':
        task_list.sort(key=get_title)
    if param_value == 'desc':
        task_list.sort(key=get_title, reverse=True)
    return jsonify(task_list), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    is_complete = complete_or_not(task)
    response = { "task":
            {"id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete}
        }
    return jsonify(response), 200


# Update: PUT
@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)
    is_complete = complete_or_not(task)

    request_body = request.get_json()
    task.title = request_body['title']
    task.description = request_body['description']
    db.session.commit()
    response = {"task":
    {   "id": task.task_id,
        "title": task.title ,
        "description": task.description,
        "is_complete": is_complete } 
        }
    return jsonify(response), 200

# request body will have { 'id': 1, 'is_complete' = false}
# completed_at = db.Column(db.DateTime, default=None) 


@task_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def mark_task_completed(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    # try:
        # need to mark the task as completed, and update this in the record
        # and save in the data base
    task.completed_at = datetime.datetime.now()  # do I need to somehow use  datetime.utcnow()?
    is_complete = complete_or_not(task)
    db.session.commit()
    response = {"task":
    {   "id": task.task_id,
        "title": task.title ,
        "description": task.description,
        "is_complete": is_complete }
        }
    bot_token = 'Bearer '+ os.environ.get('SLACK_BOT_TOKEN')
    print(bot_token)
    slack = requests.post('https://slack.com/api/chat.postMessage', headers={'Authorization': bot_token}, params={'channel': 'task-notifications', 'text':f'Someone just completed the task {task.title}', 'format': 'json'})
    # print(slack)
    # print(slack.content)
    # print('*****')
    return jsonify(response), 200


    # requests.patch(url, data=None, **kwargs)[source]

    # 'message': f"Someone just completed the task {task.title}"

@task_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.completed_at = None
    is_complete = False
    db.session.commit()
    response = {"task":
    {   "id": task.task_id,
        "title": task.title ,
        "description": task.description,
        "is_complete": is_complete } 
        }
    return jsonify(response), 200




# request body:
#        { "title": "Updated Task Title",
#         "description": "Updated Test Description"}

#response_body == {"task": {
#             "id": 1,
#             "title": "Updated Task Title",
#             "description": "Updated Test Description",
#             "is_complete": False
#         } }, 200


# Delete: DELETE
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    response = {'details': f'Task {task.task_id} "{task.title}" successfully deleted'}
    return jsonify(response), 200

