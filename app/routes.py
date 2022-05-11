from xml.dom import NotFoundErr
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from datetime import datetime
from app.models.task import Task
from app.models.goal import Goal
import app.models.common as c
import os
import requests


task_bp = Blueprint('tasks', __name__, url_prefix = '/tasks')
goal_bp = Blueprint('goals', __name__, url_prefix = '/goals')

@task_bp.route('', methods = ['GET'])
def get_all_tasks():
    if not request.args:
        return jsonify([task.to_json() for task in Task.query.all()]), 200
    return jsonify(c.get_filtered_and_sorted(Task, request.args)), 200

@task_bp.route('', methods = ['POST'])
def create_task():
    try:
        new_task = Task.new_task(request.get_json())
    except ValueError:
        abort(make_response(jsonify({"details": "Invalid data"}),400))
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task.to_json()}), 201

@task_bp.route('/<task_id>', methods = ['GET'])
def get_task_by_id(task_id):
    try:
        task = c.validate_and_get_by_id(Task, task_id)
    except ValueError:
        abort(make_response(jsonify(f"{task_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A task with id of {task_id} was not found."),404))

    return jsonify({'task': task.to_json()}), 200

@task_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id):
    try:
        task = c.validate_and_get_by_id(Task, task_id)
    except ValueError:
        abort(make_response(jsonify(f"{task_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A task with id of {task_id} was not found."),404))
    
    # TODO: refactor below into Task model as instance method
    updated_details = request.get_json()
    
    for k,v in updated_details.items():
        setattr(task, k, v)
    
    db.session.commit()

    return jsonify({'task': task.to_json()}), 200

@task_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id):
    try:
        task = c.validate_and_get_by_id(Task, task_id)
    except ValueError:
        abort(make_response(jsonify(f"{task_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A task with id of {task_id} was not found."),404))
    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': f'Task {task_id} "{task.title}" successfully deleted'}), 200

@task_bp.route('/<task_id>/mark_complete', methods = ['PATCH'])
def mark_task_complete(task_id):
    try:
        task = c.validate_and_get_by_id(Task, task_id)
    except ValueError:
        abort(make_response(jsonify(f"{task_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A task with id of {task_id} was not found."),404))
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
    try:
        task = c.validate_and_get_by_id(Task, task_id)
    except ValueError:
        abort(make_response(jsonify(f"{task_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A task with id of {task_id} was not found."),404))
    task.completed_at = None
    db.session.commit()

    return jsonify({'task': task.to_json()}), 200

# GOAL routes

@goal_bp.route('', methods = ['GET'])
def get_all_goals():
    if not request.args:
        return jsonify([goal.to_json() for goal in Goal.query.all()]), 200
    return jsonify(c.get_filtered_and_sorted(Goal, request.args)), 200

@goal_bp.route('', methods = ['POST'])
def create_goal():
    goal_details = request.get_json()
    
    if 'title' not in goal_details:
        abort(make_response(jsonify({"details": "Invalid data"}),400))
    
    new_goal = Goal(title = goal_details['title'])
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'goal': new_goal.to_json()}), 201

@goal_bp.route('/<goal_id>', methods = ['GET'])
def get_goal_by_id(goal_id):
    try:
        goal = c.validate_and_get_by_id(Goal, goal_id)
    except ValueError:
        abort(make_response(jsonify(f"{goal_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A goal with id of {goal_id} was not found."),404))

    return jsonify({'goal': goal.to_json()}), 200

@goal_bp.route('/<goal_id>', methods = ['PUT'])
def update_goal(goal_id):
    try:
        goal = c.validate_and_get_by_id(Goal, goal_id)
    except ValueError:
        abort(make_response(jsonify(f"{goal_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A goal with id of {goal_id} was not found."),404))
    updated_details = request.get_json()
    
    for k,v in updated_details.items():
        setattr(goal, k, v)
    
    db.session.commit()

    return jsonify({'goal': goal.to_json()}), 200

@goal_bp.route('/<goal_id>', methods = ['DELETE'])
def delete_goal(goal_id):
    try:
        goal = c.validate_and_get_by_id(Goal, goal_id)
    except ValueError:
        abort(make_response(jsonify(f"{goal_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A goal with id of {goal_id} was not found."),404))
    db.session.delete(goal)
    db.session.commit()

    return jsonify({'details': f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200

@goal_bp.route('/<goal_id>/tasks', methods = ['POST'])
def assign_tasks_to_goal(goal_id):
    try:
        goal = c.validate_and_get_by_id(Goal, goal_id)
    except ValueError:
        abort(make_response(jsonify(f"{goal_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A goal with id of {goal_id} was not found."),404))

    task_ids = request.get_json()['task_ids']
    for task_id in task_ids:
        try:
            task = c.validate_and_get_by_id(Task, task_id)
        except ValueError:
            abort(make_response(jsonify(f"{task_id} was included in request but is not a valid id. No changes made."),400))
        except LookupError:
            abort(make_response(jsonify(f"A task with id of {task_id} was not found. No changes made."),404))
        goal.tasks.append(task)
    db.session.commit()
    
    return jsonify({'id': int(goal_id), 'task_ids': task_ids}), 200

@goal_bp.route('/<goal_id>/tasks', methods = ['GET'])
def get_all_tasks_of_goal(goal_id):
    try:
        goal = c.validate_and_get_by_id(Goal, goal_id)
    except ValueError:
        abort(make_response(jsonify(f"{goal_id} is not a valid id."),400))
    except LookupError:
        abort(make_response(jsonify(f"A goal with id of {goal_id} was not found."),404))

    return jsonify(goal.to_json(include_tasks=True)), 200