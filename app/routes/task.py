from flask import Blueprint,jsonify, request, make_response, abort
from app.models.task import Task
from app import db
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os



task_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")


# creating task with using POST in our route decorator
@task_bp.route("", methods = ["POST"])
def create_task(): 
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task(title= request_body["title"],
                    description = request_body["description"])
    
    if "completed_at" in request_body:
            new_task.completed_at =  request_body["completed_at"]
            
    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify({"task":new_task.to_dict()})), 201


#get all task by using GET in route decorater 
@task_bp.route("", methods = ["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()
        
    return jsonify([task.to_dict() for task in tasks]), 200


#get one task by using GET in route decorater and aaccessing id
@task_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    if task.goal_id:
        response = {"task": {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }
    else:
        response = {"task":task.to_dict()}   
    return jsonify(response), 200


#updating task by using PUT in route decorater
@task_bp.route("/<task_id>", methods = ["PUT"])
def replace_one_task(task_id):
    request_body = request.get_json()
    task = validate_task(task_id)
    task.title = request_body["title"]
    task.description = request_body["description"]
        
    db.session.commit()
    return jsonify({"task":task.to_dict()}), 200


#deleting task by using DELETE in rout and by accessing task id
@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    chosen_task = validate_task(task_id)
    db.session.delete(chosen_task)
    db.session.commit()
    response_body = {"details": f'Task {task_id} \"Go on my daily walk 🏞\" successfully deleted'}
    return jsonify(response_body), 200


# return task "is complete" True if we use /<task_id>/mark_complete
@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def task_mark_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    vida_slack_bot(task.title)# calling my bot
    return jsonify({"task": task.to_dict()}), 200


# return task "is complete" False if we use /<task_id>/mark_incomplete   
@task_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def task_mark_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    return jsonify({"task":task.to_dict()}), 200


#validating task and using as a helper function in other functions
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))  
    chosen_task = Task.query.get(task_id)
    if not chosen_task:
        abort(make_response(jsonify({'details': f"Could not find task"}), 404))  
    return chosen_task

# creating slack Bot in wave 4 and using it in mark complete function
def vida_slack_bot(task_title):
    slack_key = os.environ.get("SLACK_BOT_TOKEN")
    url = "https://slack.com/api/chat.postMessage"
    params = {
    "token" : slack_key,
    "channel" : "task-notifications",
    "text" : f"Someone just completed the task {task_title}"
    }
    return requests.post(url, data=params).json()