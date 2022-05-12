from datetime import datetime
from xmlrpc.client import boolean

from dotenv import load_dotenv
import requests
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import os

load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate(input_id):
    try:
        int_id = int(input_id)
    except:
        abort(make_response({"message":f"Task {input_id} invalid"}, 400))
    task = Task.query.get(int_id)
    if not task:
        abort(make_response({"message":f"Task {int_id} not found"}, 404))
    return task

def send_slack_message(task, message):
    '''
    if message = completed, send slack message that task has been completed:
        "Someone just completed the task {task.title}"
    if message = incomplete, send slack message that task has been marked incomplete. 
        "The task {task.title} sent: {}"
    '''
    if message == "completed":
        send_message = f"Someone just completed the task {task.title}"
    else: 
        send_message = f"The task {task.title} sent: {message}"


    url = os.environ.get("SLACK_POST_URL")+send_message
    header_authorization = "Bearer "+os.environ.get("SLACK_AUTH_KEY")
    headers = {'Authorization': header_authorization}
    requests.post(url, headers=headers)
    return


@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(
            title=request_body["title"], 
            description=request_body["description"]
            )
        
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]

        ##try these instead of using expire:
        #return make_response({
                #     "task": new_task.to_dict()
                # }, 201)
        # return {
        #         "task": new_task.to_json()
        #     }, 200

        db.session.add(new_task)
        db.session.commit()
        # db.session.expire(new_task)

        return make_response(jsonify(new_task.single_dict()), 201)

    except KeyError:
        return make_response(jsonify({"details":"Invalid data"}), 400)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_query = request.args.get("is_complete")

    if title_query:
        tasks = Task.query.filter(Task.title.ilike("%" + title_query + "%"))
    elif description_query:
        tasks = Task.query.filter(Task.description.ilike("%" + description_query + "%"))
    elif completed_query == "false":
        tasks = Task.query.filter(Task.completed_at == None)
    elif completed_query == "true":
        tasks = Task.query.filter(Task.completed_at != None)
    elif sort_query in ("asc","desc"):
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title).all()
        else:
            tasks = Task.query.order_by(Task.title.desc()).all()
    else: 
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return make_response(jsonify(tasks_response), 200)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate(task_id)

    return make_response(jsonify(task.single_dict()), 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate(task_id)
    request_body = request.get_json()
    request_body_keys = request_body.keys()

    if "title" in request_body_keys:
        task.title = request_body["title"]
    if "description" in request_body_keys:
        task.description = request_body["description"]
    if "completed_at" in request_body_keys:
        task.completed_at = request_body["completed_at"]
    elif "is_complete" in request_body_keys:
        if request_body["is_complete"] == True:
            task.completed_at = datetime.utcnow()
            send_slack_message(task, "completed")
        elif request_body["is_complete"] == False:
            task.completed_at = None
            send_slack_message(task, "marked incomplete")

    db.session.commit()
    # db.session.expire(task)

    return make_response(jsonify(task.single_dict()), 200)

@tasks_bp.route("/<task_id>/<mark_completion>", methods=["PATCH"])
def task_completion(task_id, mark_completion):
    task = validate(task_id)
    request_body = request.get_json()

    if mark_completion == "mark_complete":
        task.completed_at = datetime.utcnow()
        send_slack_message(task, "completed")
    elif mark_completion == "mark_incomplete":
        task.completed_at = None
        send_slack_message(task, "marked incomplete")
    else:
        abort(make_response({"message":f"please use mark_complete or mark_incomplete"}, 404))
    
    db.session.commit()
    return make_response(jsonify(task.single_dict()), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate(task_id)
    
    response = {"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}
# "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify(response), 200)