from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import date
import requests
import os
from dotenv import load_dotenv
load_dotenv()



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    '''Takes in one task_id, returns the Task object if it exists, otherwise aborts.'''
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid, id must be integer"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task

def check_is_complete(task):
    '''Takes in one instance of task object, returns the value that should be assigned to is_complete for that object'''
    if task.completed_at is None:
        return False
    return True

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        is_complete = check_is_complete(task)
        tasks_response.append({"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete})
    
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks_response.sort(key=lambda t: t["title"])
    if sort_query == "desc":
        tasks_response.sort(reverse=True, key=lambda t: t["title"])
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods =["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    is_complete = check_is_complete(task)
    return {"task": {"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete}}


@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({'details': 'Invalid data'}), 400

    if "completed_at" in request_body:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])
    else: new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()
    
    is_complete = check_is_complete(new_task)
    body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title ,
            "description": new_task.description,
            "is_complete": is_complete
        }
    }

    return make_response(jsonify(body), 201)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    
    task = validate_task(task_id)
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({'details': 'Invalid data'}), 400

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit() 

    is_complete = check_is_complete(task)

    body = {
        "task": {
            "id": task.task_id,
            "title": task.title ,
            "description": task.description,
            "is_complete": is_complete
        }
    }

    return make_response(body)


@tasks_bp.route("/<task_id>/<mark>", methods=["PATCH"])
def update_completion(task_id, mark):
    task = validate_task(task_id)

    if mark == "mark_incomplete":
        is_complete = False
        task.completed_at = None
    if mark == "mark_complete":
        is_complete = True
        task.completed_at = date.today()
        API_TOKEN = os.environ.get("API_TOKEN")
        path = "https://slack.com/api/chat.postMessage"
        query_params = {"channel": "task-notifications", "text": f"Someone Just completed the task {task.title}"}
        header_info = {"Authorization" : f"Bearer {API_TOKEN}"}
        requests.post(path, params=query_params, headers=header_info)

    
    db.session.commit()
    
    body = {
        "task": {
            "id": task.task_id,
            "title": task.title ,
            "description": task.description,
            "is_complete": is_complete
        }
    }
    return make_response(body)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    
    body = {
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }

    return make_response(jsonify(body))

### Goal routes

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    '''Takes in one goal_id, returns the Goal object if it exists, otherwise aborts.'''
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"goal {goal_id} invalid, id must be integer"}, 400))
    
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"goal {goal_id} not found"}, 404))

    return goal


@goals_bp.route("", methods=["GET"])
def get_goals():
    
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({"id": goal.goal_id, "title": goal.title})
    
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals_response.sort(key=lambda t: t["title"])
    if sort_query == "desc":
        goals_response.sort(reverse=True, key=lambda t: t["title"])
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods =["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return {"goal": {"id": goal.goal_id, "title": goal.title}}


@goals_bp.route("", methods=["POST"])
def handle_goals():
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({'details': 'Invalid data'}), 400

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    
    body = {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }

    return make_response(jsonify(body), 201)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({'details': 'Invalid data'}), 400

    goal.title = request_body["title"]

    db.session.commit() 

    body = {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }

    return make_response(body)



@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    body = {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }

    return make_response(jsonify(body))

