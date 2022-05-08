from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from datetime import datetime
import requests
import os


tasks_bp = Blueprint("tasks_bp", __name__,  url_prefix="/tasks")
path="https://slack.com/api/chat.postMessage"
SLACK_API_KEY = os.environ.get("SLACK_AUTH_KEY")


def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"task {id} invalid"}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"message":f"task {id} not found"}, 404))

    return task


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    except KeyError:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        try:
            # check completed_at is a string that is a datetime
            new_task.completed_at=datetime.strptime(request_body["completed_at"], '%a, %d %b %Y %H:%M:%S %Z')
        except:
            abort(make_response({"message":f"the value of the completed_at should be in a date format: %a, %d %b %Y %H:%M:%S %Z"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query
    #does not make much sense in this particular filter-sort. But I programmed it "chained", so we can filter first and then sort filtered data
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")
    if title_query:
        tasks = tasks.filter_by(title=title_query)

    if sort_query =="sort by id descending":
        tasks=tasks.order_by(Task.task_id.desc())    
    elif sort_query=="asc":
        tasks = tasks.order_by(Task.title.asc()) 
    elif sort_query=="desc":
        tasks =tasks.order_by(Task.title.desc())

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return  task.to_dict()


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return task.to_dict(), 200


@tasks_bp.route("/<task_id>/<mark>", methods=["PATCH"])
def update_task1(task_id, mark):
    task = validate_task(task_id)

    if mark =="mark_complete":
        task.completed_at =datetime.utcnow() 
        slack_headers =  {"Authorization" : "Bearer "+SLACK_API_KEY}
        myobj={"channel" :"task-notifications",
               "text":f"Someone just completed the task {task.title}"}
        requests.post(path,data = myobj, headers=slack_headers)

    elif mark =="mark_incomplete": 
        task.completed_at =None

    db.session.commit()

    return task.to_dict(), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}