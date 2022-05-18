from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
from sqlalchemy import desc, asc
import requests, os


#instia Goals & Task  Blueprint

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")
SLACK_AUTH = os.environ.get("SLACK_API_AUTH")

#-------------------------- SLACK --------------------------#

def post_to_slack(task_identity):

    
    url = "https://slack.com/api/chat.postMessage"

    headers = {"Authorization" : f"Bearer {SLACK_AUTH}"}
    
    data = {
        "channel" : "task-notifications",
        "text" : f"Someone just completed the task {task_identity.title}"
    }

    response = requests.post(url, headers=headers, data=data)
    response_body = response.json()

    return response_body

#-------------------------- GOAL HELPER --------------------------#

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response(dict(message=f"Goal {goal_id} is not valid."), 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        return abort(make_response(dict(message=f"Goal {goal_id} is invalid."), 404))
    else:
        return goal

#-------------------------- GOAL --------------------------#

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title = request_body['title']
    )
    except:
        abort(make_response({"details":f"Invalid data"}, 400))
    
    db.session.add(new_goal)
    db.session.commit()
    return {
        "goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title,
    }},201

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_list(goal_id):
    from app.models.task import Task

    goal = validate_goal(goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        goal.tasks.append(task)

    db.session.add(goal)
    db.session.commit()

    return jsonify({"id": goal.goal_id, "task_ids": goal.task_ids()}), 200

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals_response = []

    order_goals = request.args.get("sort")
        
    if order_goals == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif order_goals == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()

    for goal in goals:
        goal_object = goal.to_dict()
        goals_response.append(goal_object["goal"])
    
    return jsonify(goals_response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal_by_id(goal_id):
    goal = validate_goal(goal_id)
    return jsonify(goal.to_dict()), 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal(goal_id):
    goal = validate_goal(goal_id)
    return goal.goal_to_task(), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def replace_goal_by_id(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return jsonify(goal.to_dict()), 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def remove_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(dict(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted'), 200)

#-------------------------- TASK HELPER --------------------------#

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(dict(message=f"Task {task_id} is not an interger."), 400))
    
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response(dict(message=f"Task {task_id} is invalid."), 404))
    else:
        return task

#-------------------------- TASK --------------------------#

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title = request_body['title'], description = request_body['description'])
    except:
        abort(make_response({"details":f"Invalid data"}, 400))
    
    if "completed_at" in request_body: new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": bool(new_task.completed_at)}},201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = request.args.get("sort")
    if task_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif task_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(
            {
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete": False 
            }
        )
    return jsonify(task_response)


@task_bp.route("/<task_identity>", methods=["GET"])
def get_one_task_by_id(task_identity):
    task = validate_task(task_identity)
    if task.goal_value:
        return jsonify(task.dict()), 200
    
    else:
        return jsonify(task.to_dict()), 200

@task_bp.route("/<task_identity>", methods=["DELETE"])
def delete_task_by_id(task_identity):
    task = validate_task(task_identity)

    db.session.delete(task)
    db.session.commit()

    return make_response(dict(details=f'Task {task.task_id} "{task.description}" successfully deleted'), 200)

@task_bp.route("/<task_identity>", methods=["PUT"])
def replace_task_by_id(task_identity):
    task = validate_task(task_identity)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return jsonify(task.to_dict()), 200

@task_bp.route("/<task_identity>/mark_complete", methods=["PATCH"])
def check_complete_by_id(task_identity):
    
    task = validate_task(task_identity)
    task.completed_at = datetime.now()
        
    db.session.commit()

    post_to_slack(task)
    return jsonify(task.to_dict()), 200

@task_bp.route("/<task_identity>/mark_incomplete", methods=["PATCH"])
def check_incomplete_by_id(task_identity):

    task = validate_task(task_identity)
    task.completed_at = None

    db.session.commit()

    return jsonify(task.to_dict()), 200


