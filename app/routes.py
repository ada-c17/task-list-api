from flask import Blueprint, jsonify, request, abort, make_response
from pytest import param
from app.models.task import Task
from app.models.goal import Goal
from app import db
import datetime
import os
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")
path = "https://slack.com/api/chat.postMessage"

#TASK ROUTES

def validate_task_id(task_id):
    try:
        task_id =  int(task_id)
    except:
        return abort(make_response(jsonify({'message': f"Invalid task: {task_id}"}), 400))
    task = Task.query.get(task_id)

    if task is None:
        return abort(make_response(jsonify({'message': f"Could not find task with id {task_id}"}), 404))
    return task       

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    if 'title' not in request_body or 'description' not in request_body:
        return {"details": "Invalid data"}, 400

    if 'completed_at' in request_body:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body['completed_at'])
    else:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": isinstance(new_task.completed_at, datetime.datetime)
    }}, 201

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    params = request.args
    task_response = []

    if "sort" in params:
        sort_order = request.args.get('sort')
        if sort_order == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_order =="desc":
            tasks = Task.query.order_by(Task.title.desc())
    
    else:
        tasks = Task.query.all()
    
    for task in tasks:
        task_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": isinstance(task.completed_at, datetime.datetime)
    })

    return jsonify(task_response), 200

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    one_task = validate_task_id(task_id)
    print(one_task.goal_id)
    if one_task.goal_id:
        response = {"goal_id": one_task.goal_id,
                    "id": one_task.task_id,
                    "title": one_task.title,
                    "description": one_task.description,
                    "is_complete": isinstance(one_task.completed_at, datetime.datetime)}
    else:
        response = {
                "id": one_task.task_id,
                "title": one_task.title,
                "description": one_task.description,
                "is_complete": isinstance(one_task.completed_at, datetime.datetime)
            }
    return jsonify({"task": response}), 200

@tasks_bp.route('/<task_id>', methods=['PUT'])
def put_one_task(task_id):
    one_task = validate_task_id(task_id)
    request_body = request.get_json()
    if 'title' not in request_body or 'description' not in request_body:
        return {
            "details": "Invalid data"
        }, 400

    one_task.title = request_body["title"]
    one_task.description = request_body["description"]

    db.session.commit()

    response = {
        "id": one_task.task_id,
        "title": one_task.title,
        "description": one_task.description,
        "is_complete": isinstance(one_task.completed_at, datetime.datetime)
    }
    return jsonify({"task": response}), 200

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    one_task = validate_task_id(task_id)
    db.session.delete(one_task)
    db.session.commit()

    return {"details": f'Task {one_task.task_id} "{one_task.title}" successfully deleted'}, 200

@tasks_bp.route('/<task_id>/<mark>', methods=['PATCH'])
def patch_one_task(task_id, mark=None):
    one_task = validate_task_id(task_id)

    if mark == "mark_complete":
        one_task.completed_at = datetime.datetime.now()
        query_params = {
                "channel": "#task-notifications",
                "text": f"Someone just completed the task {one_task.title}"
                }
        header = {"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
        requests.post(path, data=query_params, headers=header)

    elif mark == 'mark_incomplete':
        one_task.completed_at = None

    db.session.commit()

    response = {
        "id": one_task.task_id,
        "title": one_task.title,
        "description": one_task.description,
        "is_complete": isinstance(one_task.completed_at, datetime.datetime)
    }
    return jsonify({"task": response}), 200

########################################################
########################################################
#GOAL ROUTES
def validate_goal_id(goal_id):
    try:
        goal_id =  int(goal_id)
    except:
        return abort(make_response(jsonify({'message': f"Invalid task: {goal_id}"}), 400))
    goal = Goal.query.get(goal_id)

    if goal is None:
        return abort(make_response(jsonify({'message': f"Could not find task with id {goal_id}"}), 404))
    return goal     


@goals_bp.route('', methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    new_goal = Goal(title=request_body['title'])
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title
    }}, 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goal_response = []
    goals = Goal.query.all()

    for goal in goals:
        goal_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })
    return jsonify(goal_response), 200

@goals_bp.route("<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    one_goal = validate_goal_id(goal_id)
    response = {
        "id": one_goal.goal_id,
        "title": one_goal.title
    }
    return jsonify({"goal": response}), 200

@goals_bp.route("<goal_id>", methods=['PUT'])
def put_one_goal(goal_id):
    one_goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    one_goal.title = request_body["title"]
    db.session.commit()

    response = {
        "id": one_goal.goal_id,
        "title": one_goal.title
    }
    return jsonify({"goal": response}), 200

@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_one_goal(goal_id):
    one_goal = validate_goal_id(goal_id)
    db.session.delete(one_goal)
    db.session.commit()

    return {"details": f'Goal {one_goal.goal_id} "{one_goal.title}" successfully deleted'}, 200

#######################################
######################################
#GOALS + TASKS ROUTES

@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def create_task_with_goal_id(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    ids = []
    for id in request_body["task_ids"]:
        task= validate_task_id(id)
        task.goal = goal
        ids.append(id)
    
    db.session.commit()
    
    response = {
        "id": goal.goal_id,
        "task_ids": ids
    }
    return response, 200

@goals_bp.route("<goal_id>/tasks", methods=["GET"])
def get_all_task_with_goal_id(goal_id):
    goal = validate_goal_id(goal_id)
    task_response = []
    for task in goal.task:
        task_response.append(    {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": isinstance(task.completed_at, datetime.datetime)
        })

    return {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_response
    }, 200

    



