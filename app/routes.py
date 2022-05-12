import json
import os
from xmlrpc.client import boolean
import requests
from crypt import methods
from flask import Blueprint, abort, make_response, jsonify, request
from datetime import datetime
from app.models.task import Task
from app.models.goal import Goal
from app import db

task_bp = Blueprint('task_bp', __name__, url_prefix="/tasks")
goal_bp = Blueprint('goal_bp', __name__, url_prefix="/goals")

# *******************
# ROUTES FOR TASK_BP
# *******************

# helper function to determine true or false
def boolean_completed_task(task):
    if task.completed_at is None:
        task.completed_at = False
    else:
        task.completed_at = True


@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    try:
        request_body["title"] == True
        request_body["description"] == True
    except KeyError:
        rsp = {"details": "Invalid data"}
        abort(make_response(jsonify(rsp), 400))

    if 'completed_at' in request_body:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"]
        )
    else:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
        )
    

    db.session.add(new_task)
    db.session.commit()

    boolean_completed_task(new_task)

    rsp = {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at
    }}
    
    return jsonify(rsp), 201


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid ID: {task_id}"}
        abort(make_response(jsonify(rsp), 400))    
    
    selected_task = Task.query.get(task_id)
    if selected_task is None:
        rsp = {"msg": f"Could not find task with ID: {task_id}"}
        abort(make_response(jsonify(rsp), 404))

    return selected_task    


@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    selected_task = validate_task(task_id)

    boolean_completed_task(selected_task)
    
    if selected_task.goal_id:
        rsp = {
            "task": {
                "id": selected_task.task_id,
                "goal_id": selected_task.goal_id,
                "title": selected_task.title,
                "description": selected_task.description,
                "is_complete": selected_task.completed_at
            }
        }
    else:
        rsp = {
            "task": {
                "id": selected_task.task_id,
                "title": selected_task.title,
                "description": selected_task.description,
                "is_complete": selected_task.completed_at
            }
        }    
    return jsonify(rsp), 200


@task_bp.route('', methods=['GET'])
def get_all_tasks():
    sort_tasks = request.args.get("sort")

    tasks = Task.query.all()
    tasks_response = []

    

    for task in tasks:
        boolean_completed_task(task)  
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at
        })
    if sort_tasks:
        if sort_tasks == "asc":
            return jsonify(sorted(tasks_response, key=lambda a: a["title"])), 200
        elif sort_tasks == "desc":
            return jsonify(sorted(tasks_response, key=lambda a: a["title"], reverse=True)), 200
    return jsonify(tasks_response), 200    


@task_bp.route('/<task_id>', methods=['PUT'])
def put_one_task(task_id):
    selected_task = validate_task(task_id)
    request_body = request.get_json()
    try:
        selected_task.title = request_body["title"]
        selected_task.description = request_body["description"]
    except KeyError:
        return {"details": "Invalid data"}, 400   
    db.session.commit()

    boolean_completed_task(selected_task)
    rsp = {
        "task": {
            "id": selected_task.task_id,
            "title": selected_task.title,
            "description": selected_task.description,
            "is_complete": selected_task.completed_at
        }
    }
    return jsonify(rsp), 200


@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    selected_task = validate_task(task_id)

    db.session.delete(selected_task)
    db.session.commit()

    return {
        "details": 
        f'Task {selected_task.task_id} \"{selected_task.title}" successfully deleted'}, 200


# frankly, I'd love to be able to merge this function 
# and the one below into a singular function. and just use two route decorators
# until I can figure that out though, I'm separating them into two
@task_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    selected_task = validate_task(task_id)

    selected_task.completed_at = datetime.utcnow()
    db.session.commit()

    boolean_completed_task(selected_task)
    rsp = {
        "task": {
            "id": selected_task.task_id,
            "title": selected_task.title,
            "description": selected_task.description,
            "is_complete": selected_task.completed_at
        }
    }

    # Slack bot message posting
    channel_id = "C03FG8SA2LR"
    api_key = "Bearer " + os.environ.get("SLACK_BOT_API_KEY")
    post_message_url = "https://slack.com/api/chat.postMessage"
    post_message_params = {
        "channel": channel_id, 
        "text": f"Someone just completed the task {selected_task.title}"}
    post_message_headers = {
        "Authorization": api_key
    }
    requests.post(post_message_url, params=post_message_params, headers=post_message_headers)
    return jsonify(rsp), 200


# ditto above
@task_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    selected_task = validate_task(task_id)
    
    selected_task.completed_at = None
    db.session.commit()

    boolean_completed_task(selected_task)
    rsp = {
        "task": {
            "id": selected_task.task_id,
            "title": selected_task.title,
            "description": selected_task.description,
            "is_complete": selected_task.completed_at
        }
    }
    return jsonify(rsp), 200


# *******************
# ROUTES FOR GOAL_BP
# *******************

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        rsp = {"msg": f"Invalid ID: {goal_id}"}
        abort(make_response(jsonify(rsp), 400))    
    
    selected_goal = Goal.query.get(goal_id)
    if selected_goal is None:
        rsp = {"msg": f"Could not find goal with ID: {goal_id}"}
        abort(make_response(jsonify(rsp), 404))

    return selected_goal   


@goal_bp.route('', methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    try:
        request_body["title"] == True
    except KeyError:
        rsp = {"details": "Invalid data"}
        abort(make_response(jsonify(rsp), 400))

    new_goal = Goal(
        title = request_body["title"]
    )   
    
    db.session.add(new_goal)
    db.session.commit()

    rsp = {"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title,
    }}

    return jsonify(rsp), 201


@goal_bp.route('', methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
            })
    
    return jsonify(goals_response), 200


@goal_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    selected_goal = validate_goal(goal_id)

    rsp = {"goal": {
        "id": selected_goal.goal_id,
        "title": selected_goal.title,
    }}

    return jsonify(rsp), 200


@goal_bp.route('/<goal_id>', methods=['PUT'])
def update_one_goal(goal_id):
    selected_goal = validate_goal(goal_id)
    request_body = request.get_json()
    try:
        selected_goal.title = request_body["title"]
    except KeyError:
        return {"details": "Invalid data"}, 400   
    db.session.commit()

    rsp = {"goal": {
        "id": selected_goal.goal_id,
        "title": selected_goal.title,
    }}

    return jsonify(rsp), 200


@goal_bp.route('/<goal_id>', methods=['DELETE'])
def delete_one_goal(goal_id):
    selected_goal = validate_goal(goal_id)

    db.session.delete(selected_goal)
    db.session.commit()

    return {"details": 
        f'Goal {selected_goal.goal_id} \"{selected_goal.title}" successfully deleted'}, 200


# *******************
# NESTED ROUTES
# *******************

@goal_bp.route('/<goal_id>/tasks', methods=['POST'])
def post_tasks_to_goal(goal_id):
    selected_goal = validate_goal(goal_id)
    request_body = request.get_json()

    try:
        request_body["task_ids"] == True
    except KeyError:
        rsp = {"details": "Invalid data"}
        abort(make_response(jsonify(rsp), 400))

    task_list = []

    for task in request_body["task_ids"]:
        selected_task = validate_task(task)
        selected_task.goal_id = goal_id
        task_list.append(task)

    db.session.commit()
    rsp = {
        "id": selected_goal.goal_id,
        "task_ids": task_list
    }
    return jsonify(rsp), 200

@goal_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_tasks_of_one_goal(goal_id):
    selected_goal = validate_goal(goal_id)

    task_list = []
    for task in selected_goal.tasks:
        selected_task = validate_task(task.task_id)
        boolean_completed_task(selected_task)
        task_list.append({
            "id": selected_task.task_id,
            "goal_id": selected_task.goal_id,
            "title": selected_task.title,
            "description": selected_task.description,
            "is_complete": selected_task.completed_at
        })

    rsp = {
        "id": selected_goal.goal_id,
        "title": selected_goal.title,
        "tasks": task_list
    }
    return jsonify(rsp), 200

