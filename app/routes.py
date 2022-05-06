from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
from datetime import datetime
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_element(element_id):
    try:
        element_id = int(element_id)
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    if request.blueprint == "tasks":
        element = Task.query.get(element_id)
        name = "Task"
    elif request.blueprint == "goals":
        element = Goal.query.get(element_id)
        name = "Goal"

    if not element:
        return abort(make_response({"message" : f"{name} {element_id} is not found"}, 404))
    return element


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    
    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = validate_element(task_id)
    return jsonify({"task": task.to_json()}), 200


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.create_task(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201

@tasks_bp.route("<task_id>", methods=['PUT'])
def update_one_task(task_id):
    task = validate_element(task_id)
    request_body = request.get_json()

    task.title = request_body['title']
    task.description = request_body['description']

    db.session.commit()
    
    return make_response(jsonify({"task" : task.to_json()}), 200)

@tasks_bp.route('<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = validate_element(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200)

@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    task = validate_element(task_id)
    
    task.completed_at = datetime.now()
    db.session.commit()

    slack_api_url = "https://slack.com/api/chat.postMessage"
    params = {
        "channel" : "task-notifications",
        "text" : f"Someone just completed the task {task.title}"
    }
    headers = {
        "Authorization" : f"Bearer {os.environ.get('SLACK_API_HEADER')}"
    }
    requests.get(url=slack_api_url, params=params, headers=headers)
    
    return make_response(jsonify({"task" : task.to_json()}))

@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = validate_element(task_id)

    task.completed_at = None
    db.session.commit()

    return make_response(jsonify({"task" : task.to_json()}))



#Goals Routes
@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())
    
    return make_response(jsonify(goals_response), 200)

@goals_bp.route("<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_element(goal_id)
    return jsonify({"goal": goal.to_json()}), 200

@goals_bp.route("", methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    new_goal = Goal.create_task(request_body)
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_json()}), 201

@goals_bp.route("<goal_id>", methods=['PUT'])
def update_one_goal(goal_id):
    goal = validate_element(goal_id)
    request_body = request.get_json()

    goal.title = request_body['title']

    db.session.commit()
    
    return make_response(jsonify({"goal" : goal.to_json()}), 200)

@goals_bp.route('<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_element(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200)