from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.task import Task
from .helper import validate_client_requests, validate_task
from datetime import datetime
import requests, os # for Slackbot proj

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#Get all 
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_sorted_query = request.args.get("sort")
    if title_sorted_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif title_sorted_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response),200


#Get one
@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return {"task": task.to_json()}, 200


#Create one
@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = validate_client_requests(request_body)
    db.session.add(new_task)
    db.session.commit()
    return {"task": new_task.to_json()}, 201
    
    # or without helper function:
    #request_body = request.get_json()
    #if "title" in request_body and "description" in request_body:
    #     new_task = Task.create(request_body)
    #     db.session.add(new_task)
    #     db.session.commit()
    # else:
    #     return  {"details": "Invalid data"}, 400
    

#Update one - PUT
@tasks_bp.route("/<id>", methods=["PUT"])
def update_one_task(id):
    task = validate_task(id)
    request_body = request.get_json()
#    response = client.put("/tasks/1", json={
#         "title": "Updated Task Title",
#         "description": "Updated Test Description",
#         "completed_at": datetime.utcnow() or None
#     })
    task.update(request_body)
        # >>> def update(self, req_body):       
        # >>>>>> self.title = req_body["title"],
        # >>>>>> self.description = req_body["description"]
    db.session.commit()
    return {"task": task.to_json()}, 200


#Delete one
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task = validate_task(id)
    db.session.delete(task)
    db.session.commit()
    return {"details": f'Task {id} "Go on my daily walk 🏞" successfully deleted'}


#Patch: mark complete 
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete_on_incomplete_task(id):
    task = validate_task(id)
    # request_body = request.get_json() 
    # -  Why dont need request_body, bc I got the task needs to be \
    #   update from line 79. task.completed_at = None bc it was \
    #   incompleted and request to change to completed (assign time value)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    # return make_response({"task": task.to_json()}), 200
    return {"task": task.to_json()}, 200

#Patch:mark imcomplete 
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_on_complete_task(id):
    task = validate_task(id)
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_json()}, 200


def slackbot():
    """
    client marks complete, slack bot will auto send a message 
    task6 My beautiful task
    patch: tasks/6/mark_complete
    """
    #steps
    #1. import requests
    #2. path = "https://slack.com/api/chat.postMessage"
    #3. SLACK_API_KEY 
    # #4.query_params = {
    # "token": SLACK_API__KEY,
    # "channel": "task-notifications",
    # "format": "json"
    # }
    #4. text = "Someone just completed the task My Beautiful Task"
    # response = requests.post(path, params = query_params)

    # print 


    message = "Someone just completed the task My Beautiful Task"

    path = "https://slack.com/api/chat.postMessage"

    SLACK_API_KEY = os.environ.get(SLACK_API_KEY)

    query_params = {
    "token": SLACK_API_KEY,
    "channel": "task-notifications",
    "text": message,
    "format": "json"
    }

    response = mark_complete_on_incomplete_task(6)
    if response.status_code == 200:
        requests.post(path, params=query_params)
    response_for_slackbot = requests.post(path, params=query_params)
    print(response_for_slackbot.json())

slackbot()


