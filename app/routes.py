from flask import Blueprint, jsonify, request 
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc, asc
from datetime import datetime
import requests
import os



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return jsonify({"msg" : f"'{task_id}' is invalid"}), 400
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message" : f"Could not find '{task_id}'"}), 404
    return task

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return jsonify({"msg" : f"'{goal_id}' is invalid"}), 400

    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify({"message" : f"Could not find '{goal_id}'"}), 404
    return goal


def format_task(task):
    return {
    "task" : 
        {
            "is_complete" : bool(task.completed_at),
            "description" : task.description,
            "title" : task.title,
            "id" : task.task_id
        }
    }


def format_goal(goal):
    return {
        "goal": {
            "id" : goal.goal_id,
            "title" : goal.title
                }
        }


def push_complete_to_slack(task):
    bot_token = os.environ.get("SLACK_BOT_TOKEN")
    params = {
        "channel" : "task-notifications", 
        "text" : f"Someone just completed the task {task.title}"
        }
    headers = {"authorization" : "Bearer " + bot_token}
    requests.post("https://slack.com/api/chat.postMessage", params=params, headers=headers)


@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        return {
            "details" : "Invalid data"
        }, 400

    new_task = Task(
        description = request_body['description'],
        title = request_body['title']
    )

    if "completed_at" in request_body:
        new_task.completed_at = request_body['completed_at']

    db.session.add(new_task)
    db.session.commit()
    
    return format_task(new_task), 201


@tasks_bp.route('', methods=['GET'])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.order_by(asc(Task.title)).all()

    tasks_response = []

    for task in tasks:
        tasks_response.append(
            {
                "is_complete" : bool(task.completed_at),
                "description" : task.description,
                "title" : task.title,
                "id" : task.task_id
            }
        )

    return jsonify(tasks_response), 200


@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)

    if isinstance(task, Task):
        return format_task(task), 200
    return task


@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    if isinstance(task, Task):
        task.title = request_body["title"]
        task.description = request_body["description"]
        db.session.commit()

        if "completed_at" in request_body:
            task.completed_at = request_body['completed_at']

        return format_task(task), 200
    return task

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = validate_task(task_id)
    if isinstance(task, Task):
        db.session.delete(task)
        db.session.commit()
        return {
            "details" : f'Task {task_id} "{task.title}" successfully deleted'
        }
    return task

@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete(task_id):
    task = validate_task(task_id)

    if isinstance(task, Task):

        task.completed_at = datetime.utcnow()
        db.session.commit()
        push_complete_to_slack(task)
        return format_task(task), 200
    return task

@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    if isinstance(task, Task):
        task.completed_at = None
        db.session.commit()
        return format_task(task), 200
    return task

@goals_bp.route('', methods=['POST'])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {
            "details" : "Invalid data"
        }, 400

    new_goal = Goal(
        title = request_body['title']
    )

    db.session.add(new_goal)
    db.session.commit()

    return format_goal(new_goal), 201

@goals_bp.route('', methods=['GET'])
def get_goals():
    goals = Goal.query.order_by(asc(Goal.title)).all()
    goals_response = []

    for goal in goals:
        goals_response.append(
            {
            "id" : goal.goal_id,
            "title" : goal.title
            }
        )
    return jsonify(goals_response), 200

@goals_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    if isinstance(goal, Goal):
        return format_goal(goal), 200
    return goal

@goals_bp.route('/<goal_id>', methods=['PUT'])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    if isinstance(goal, Goal):
        goal.title = request_body["title"]
        db.session.commit()
        
        return format_goal(goal), 200
    return goal

@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    if isinstance(goal, Goal):
        db.session.delete(goal)
        db.session.commit()
        return {
            "details" : f'Goal {goal_id} "{goal.title}" successfully deleted'
        }
    return goal

    
