from sqlalchemy import Integer, asc, desc, cast
from app import db
from app.models.task import Task 
from app.models.goal import Goal 
from flask import Blueprint, abort, jsonify, make_response, request
import datetime
from sqlalchemy.sql.functions import now 
import requests, os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


##### Task Model #####
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {
        "details": "Invalid data"
    }, 400

    new_task = Task(title=request_body["title"],
                    description=request_body["description"]
                    )

    if "completed_at" in request_body:
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "task": new_task.to_dict()
        }), 201


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    task_query = request.args
    if "title" in task_query:
        title_name = task_query["title"]
        tasks = Task.query.filter_by(title=title_name)
    elif "sort" in task_query:
        if task_query["sort"] == "desc":
            tasks = Task.query.order_by(desc(Task.title)).all()
        elif task_query["sort"] == "asc": 
            tasks = Task.query.order_by(asc(Task.title)).all()
        elif task_query["sort"] == "id":
            tasks = Task.query.order_by(cast(Task.task_id, Integer)).all()
        # elif "title" in task_query:
        # driver_name = task_query["driver"]
        # cars = Task.query.filter_by(driver=driver_name)
        
    else:
        tasks = Task.query.all()
    # task_query = request.args
    # if "sort" in task_query:
    #     if task_query["sort"] == "desc":
    #         tasks = Task.query.order_by(desc(Task.title)).all()
    #     else: 
    #         tasks = Task.query.order_by(asc(Task.title)).all()
    # elif "sort" in task_query:
    #     if task_query["sort"] == "id":
    #         tasks = Task.query.order_by(cast(Task.task_id, Integer)).all()
    # else:
    #     tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    return jsonify(tasks_response)


# helper function:
def validate_task(id_of_task):
    try:
        id_of_task = int(id_of_task)
    except:
        abort(make_response({"message":f"task {id_of_task} invalid"}, 400))

    chosen_task = Task.query.get(id_of_task)

    if not chosen_task:
        abort(make_response({"message":f"task {id_of_task} not found"}, 404))

    return chosen_task


@tasks_bp.route("/<id_of_task>", methods=["GET"])
def read_one_task(id_of_task):
    task = validate_task(id_of_task)
    return jsonify({
        "task": task.to_dict()
        }), 200
    

@tasks_bp.route("/<id_of_task>", methods=["PUT"])
def replace_task(id_of_task):
    task = validate_task(id_of_task)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({
        "task": task.to_dict()
        }), 200


@tasks_bp.route("/<id_of_task>/mark_complete", methods=["PATCH"])
def update_task_complete(id_of_task):
    task = validate_task(id_of_task)
    task.completed_at = datetime.datetime.now()

    db.session.commit()

    SLACK_API_URL = "https://slack.com/api/chat.postMessage"
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    headers={"Authorization": SLACK_BOT_TOKEN}

    url = requests.post(SLACK_API_URL, headers=headers, params=query_params)

    return jsonify({
        "task": task.to_dict()
        }), 200


@tasks_bp.route("/<id_of_task>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(id_of_task):
    task = validate_task(id_of_task)
    task.completed_at = None 

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "task": task.to_dict()
        }), 200


@tasks_bp.route("/<id_of_task>", methods=["DELETE"])
def delete_task(id_of_task):
    task = validate_task(id_of_task)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task 1 "{task.title}" successfully deleted'
    }
    