from urllib.parse import urlencode
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from datetime import datetime
from app.models.task import Task
from app.models.goal import Goal
import os
import requests
# from dotenv import load_dotenv

# load_dotenv()

task_bp = Blueprint('tasks', __name__, url_prefix = '/tasks')
goal_bp = Blueprint('goals', __name__, url_prefix = '/goals')

@task_bp.route('', methods = ['GET'])
def get_all_tasks():
    if not request.args:
        all_tasks = [task.to_json() for task in Task.query.all()]
    else:
        params = dict(request.args)
        sort_style = params.pop('sort', None)
        if sort_style and len(params) > 0:
            all_tasks = [task.to_json() for task in Task.query.filter_by(**params).order_by(getattr(Task.title,sort_style)())]
        elif sort_style:
            all_tasks = [task.to_json() for task in Task.query.order_by(getattr(Task.title,sort_style)())]
        else:
            all_tasks = [task.to_json() for task in Task.query.filter_by(**params)]

    return jsonify(all_tasks), 200

@task_bp.route('', methods = ['POST'])
def create_task():
    task_details = request.get_json()
    # Validate and clean input
    if 'title' not in task_details or 'description' not in task_details:
        abort(make_response(jsonify({"details": "Invalid data"}),400))
    if 'completed_at' not in task_details:
        task_details['completed_at'] = None
    
    new_task = Task(
        title = task_details['title'],
        description = task_details['description'],
        completed_at = task_details['completed_at']
        )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task.to_json()}), 201

@task_bp.route('/<task_id>', methods = ['GET'])
def get_task_by_id(task_id):
    task = Task.validate_id(task_id)

    return jsonify({'task': task.to_json()}), 200

@task_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id):
    task = Task.validate_id(task_id)
    updated_details = request.get_json()
    
    for k,v in updated_details.items():
        setattr(task, k, v)
    
    db.session.commit()

    return jsonify({'task': task.to_json()}), 200

@task_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = Task.validate_id(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': f'Task {task_id} "{task.title}" successfully deleted'}), 200

@task_bp.route('/<task_id>/mark_complete', methods = ['PATCH'])
def mark_task_complete(task_id):
    task = Task.validate_id(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    headers = {'Authorization': f'Bearer {os.environ.get("SLACKBOT_OAUTH_TOKEN")}'}
    params = {
        'text': f'Someone just completed the task {task.title}',
        'channel': 'task-notifications'
    }
    r = requests.post(
        'https://slack.com/api/chat.postMessage', 
        params = params, 
        headers = headers
    )

    return jsonify({'task': task.to_json()}), 200

@task_bp.route('/<task_id>/mark_incomplete', methods = ['PATCH'])
def mark_task_incomplete(task_id):
    task = Task.validate_id(task_id)
    task.completed_at = None
    db.session.commit()

    return jsonify({'task': task.to_json()}), 200

# GOAL routes

@goal_bp.route('', methods = ['GET'])
def get_all_goals():
    if not request.args:
        all_goals = [goal.to_json() for goal in Goal.query.all()]
    else:
        params = dict(request.args)
        sort_style = params.pop('sort', None)
        if sort_style and len(params) > 0:
            all_goals = [goal.to_json() for goal in Goal.query.filter_by(**params).order_by(getattr(Goal.title,sort_style)())]
        elif sort_style:
            all_goals = [goal.to_json() for goal in Goal.query.order_by(getattr(Goal.title,sort_style)())]
        else:
            all_goals = [goal.to_json() for goal in Goal.query.filter_by(**params)]

    return jsonify(all_goals), 200

@goal_bp.route('', methods = ['POST'])
def create_goal():
    goal_details = request.get_json()
    # Validate and clean input
    if 'title' not in goal_details:
        abort(make_response(jsonify({"details": "Invalid data"}),400))
    
    new_goal = Goal(title = goal_details['title'])
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'goal': new_goal.to_json()}), 201

@goal_bp.route('/<goal_id>', methods = ['GET'])
def get_goal_by_id(goal_id):
    goal = Goal.validate_id(goal_id)

    return jsonify({'goal': goal.to_json()}), 200

@goal_bp.route('/<goal_id>', methods = ['PUT'])
def update_goal(goal_id):
    goal = Goal.validate_id(goal_id)
    updated_details = request.get_json()
    
    for k,v in updated_details.items():
        setattr(goal, k, v)
    
    db.session.commit()

    return jsonify({'goal': goal.to_json()}), 200

@goal_bp.route('/<goal_id>', methods = ['DELETE'])
def delete_goal(goal_id):
    goal = Goal.validate_id(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return jsonify({'details': f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200
