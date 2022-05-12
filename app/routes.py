from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from datetime import datetime
from app.models.task import Task
from app.models.goal import Goal, TasksGoal
from app.models.common import (MissingValueError, FormatError, DBLookupError,
                IDTypeError, validate_and_get_by_id, get_filtered_and_sorted)
from app.error_responses import make_error_response
import os
import requests


task_bp = Blueprint('tasks', __name__, url_prefix = '/tasks')
goal_bp = Blueprint('goals', __name__, url_prefix = '/goals')


@task_bp.route('', methods = ['GET'])
def get_tasks():
    if not request.args:
        return jsonify(Task.query.all())
    return jsonify(get_filtered_and_sorted(Task, request.args)), 200

@task_bp.route('', methods = ['POST'])
def create_task():
    try:
        new_task = Task.new_task(request.get_json())
    except (MissingValueError, FormatError) as err:
        abort(make_error_response(err, Task))
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task}), 201

@task_bp.route('/<task_id>', methods = ['GET'])
def get_task_by_id(task_id):
    try:
        task = validate_and_get_by_id(Task, task_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Task, task_id))
    return jsonify({'task': task}), 200

@task_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id):
    try:
        task = validate_and_get_by_id(Task, task_id)
        task.update(request.get_json())
    except (IDTypeError, DBLookupError, FormatError) as err:
        abort(make_error_response(err, Task, task_id))
    
    db.session.commit()
    return jsonify({'task': task}), 200

@task_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id):
    try:
        task = validate_and_get_by_id(Task, task_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Task, task_id))
    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': f'Task {task_id} "{task.title}" successfully deleted'}), 200

@task_bp.route('/<task_id>/mark_complete', methods = ['PATCH'])
def mark_task_complete(task_id):
    try:
        task = validate_and_get_by_id(Task, task_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Task, task_id))
    task.completed_at = datetime.utcnow()
    db.session.commit()

    #TODO: refactor slack notification out of routes
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

    return jsonify({'task': task}), 200

@task_bp.route('/<task_id>/mark_incomplete', methods = ['PATCH'])
def mark_task_incomplete(task_id):
    try:
        task = validate_and_get_by_id(Task, task_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Task, task_id))
    task.completed_at = None
    db.session.commit()

    return jsonify({'task': task}), 200

# ##############################################################  GOAL routes

@goal_bp.route('', methods = ['GET'])
def get_all_goals():
    if not request.args:
        return jsonify(Goal.query.all()), 200
    return jsonify(get_filtered_and_sorted(Goal, request.args)), 200

@goal_bp.route('', methods = ['POST'])
def create_goal():
    #TODO: refactor create new goal as class method
    goal_details = request.get_json()
    
    if 'title' not in goal_details:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
    
    new_goal = Goal(title = goal_details['title'])
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'goal': new_goal}), 201

@goal_bp.route('/<goal_id>', methods = ['GET'])
def get_goal_by_id(goal_id):
    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))

    return jsonify({'goal': goal}), 200

@goal_bp.route('/<goal_id>', methods = ['PUT'])
def update_goal(goal_id):
    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))
    
    #TODO: refactor update into instance method
    updated_details = request.get_json()
    
    for k,v in updated_details.items():
        setattr(goal, k, v)
    
    db.session.commit()

    return jsonify({'goal': goal}), 200

@goal_bp.route('/<goal_id>', methods = ['DELETE'])
def delete_goal(goal_id):
    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))
    db.session.delete(goal)
    db.session.commit()

    return jsonify({'details': f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200

@goal_bp.route('/<goal_id>/tasks', methods = ['POST'])
def assign_tasks_to_goal(goal_id):
    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))

    task_ids = request.get_json()['task_ids']
    for task_id in task_ids:
        try:
            task = validate_and_get_by_id(Task, task_id)
        except (IDTypeError, DBLookupError) as err:
            abort(make_error_response(err, Task, task_id, detail=' No changes were made.'))
        goal.tasks.append(task)
    db.session.commit()
    
    return jsonify({'id': int(goal_id), 'task_ids': task_ids}), 200

@goal_bp.route('/<goal_id>/tasks', methods = ['GET'])
def get_all_tasks_of_goal(goal_id):
    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))
    
    return jsonify(TasksGoal(goal)), 200