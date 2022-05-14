from typing import Literal
from flask import Blueprint, Response, jsonify, request, abort
from app import db
from datetime import datetime
from app.models.task import Task
from app.models.goal import Goal, TasksGoal
from app.commons import (validate_and_get_by_id, get_filtered_and_sorted,
                        notify, make_slackbot_response)
from app.error_responses import (MissingValueError, FormatError, DBLookupError,
                                IDTypeError, make_error_response)
import re

QueryParam = str  # for type annotations

###############
# Task routes #
###############

task_bp = Blueprint('tasks', __name__, url_prefix = '/tasks')

@task_bp.route('', methods = ['GET'])
def get_tasks() -> tuple[Response, Literal[200]]:
    '''Queries DB for Tasks and returns result as JSON data.'''

    if not request.args:
        return jsonify(Task.query.all()), 200
    return jsonify(get_filtered_and_sorted(Task, request.args)), 200

@task_bp.route('', methods = ['POST'])
def create_task() -> tuple[Response, Literal[201]]:
    '''Passes request JSON data to Task.create() and saves result to DB.
    
    Returns details of created Task instance as JSON data.
    '''

    try:
        new_task = Task.create(request.get_json())
    except (MissingValueError, FormatError) as err:
        abort(make_error_response(err, Task))
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task}), 201

@task_bp.route('/<task_id>', methods = ['GET'])
def get_task_by_id(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Task and returns details as JSON data.'''

    try:
        task = validate_and_get_by_id(Task, task_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Task, task_id))
    
    return jsonify({'task': task}), 200

@task_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Passes request JSON data to Task.update() and saves result to DB.
    
    Returns details of updated Task instance as JSON data.
    '''

    try:
        task = validate_and_get_by_id(Task, task_id)
        task.update(request.get_json())
    except (IDTypeError, DBLookupError, FormatError) as err:
        abort(make_error_response(err, Task, task_id))
    db.session.commit()

    return jsonify({'task': task}), 200

@task_bp.route('/<task_id>', methods = ['DELETE'])
def delete_task(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Task instance and deletes it if found.'''

    try:
        task = validate_and_get_by_id(Task, task_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Task, task_id))
    db.session.delete(task)
    db.session.commit()

    return jsonify({'details': (f'Task {task_id} "{task.title}" '
                                f'successfully deleted')}), 200

@task_bp.route('/<task_id>/mark_complete', methods = ['PATCH'])
def mark_task_complete(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Sets value of completed_at attribute on specified Task instance.
    
    Returns details of updated Task instance as JSON data.
    '''

    try:
        task = validate_and_get_by_id(Task, task_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Task, task_id))
    
    task.completed_at = datetime.utcnow()
    db.session.commit()
    notify(task.title, 'mark_complete') # Slack notification

    return jsonify({'task': task}), 200

@task_bp.route('/<task_id>/mark_incomplete', methods = ['PATCH'])
def mark_task_incomplete(task_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Unsets value of completed_at attribute on specified Task instance.
    
    Returns details of updated Task instance as JSON data.
    '''
    try:
        task = validate_and_get_by_id(Task, task_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Task, task_id))
    
    task.completed_at = None
    db.session.commit()
    notify(task.title, 'mark_incomplete') # Slack notification

    return jsonify({'task': task}), 200


###############
# Goal routes #
###############

goal_bp = Blueprint('goals', __name__, url_prefix = '/goals')

@goal_bp.route('', methods = ['GET'])
def get_all_goals() -> tuple[Response, Literal[200]]:
    '''Queries DB for Goals and returns result as JSON data.'''

    if not request.args:
        return jsonify(Goal.query.all()), 200
    return jsonify(get_filtered_and_sorted(Goal, request.args)), 200

@goal_bp.route('', methods = ['POST'])
def create_goal() -> tuple[Response, Literal[201]]:
    '''Passes request JSON data to Goal.create() and saves result to DB.
    
    Returns details of created Goal instance as JSON data.
    '''

    try:
        new_goal = Goal.create(request.get_json())
    except MissingValueError as err:
        abort(make_error_response(err, Goal))
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'goal': new_goal}), 201

@goal_bp.route('/<goal_id>', methods = ['GET'])
def get_goal_by_id(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Goal and returns basic info as JSON data.'''

    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))

    return jsonify({'goal': goal}), 200

@goal_bp.route('/<goal_id>', methods = ['PUT'])
def update_goal(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Passes request JSON data to Goal.update() and saves result to DB.
    
    Returns details of updated Goal instance as JSON data.
    '''

    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))
    
    goal.update(request.get_json())
    db.session.commit()

    return jsonify({'goal': goal}), 200

@goal_bp.route('/<goal_id>', methods = ['DELETE'])
def delete_goal(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Goal instance and deletes it if found.'''

    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))
    db.session.delete(goal)
    db.session.commit()

    return jsonify({'details': (f'Goal {goal_id} "{goal.title}" '
                                f'successfully deleted')}), 200


###################################################
# Nested routes - Task actions accessed via goals #
###################################################

@goal_bp.route('/<goal_id>/tasks', methods = ['POST'])
def assign_tasks_to_goal(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Assigns one or more Tasks to the specified Goal.
    
    A list of Task IDs is expected as JSON data in the request body. If any
    ID value is invalid, or if not all specified Tasks can be found, no changes
    are saved.
    '''

    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))
    
    task_ids = request.get_json()['task_ids']
    for task_id in task_ids:
        try:
            task = validate_and_get_by_id(Task, task_id)
        except (IDTypeError, DBLookupError) as err:
            abort(make_error_response(err, Task, task_id, 
                                        detail=' No changes were made.'))
        goal.tasks.append(task)
    db.session.commit()
    
    return jsonify({'id': int(goal_id), 'task_ids': task_ids}), 200

@goal_bp.route('/<goal_id>/tasks', methods = ['GET'])
def get_all_tasks_of_goal(goal_id: QueryParam) -> tuple[Response, Literal[200]]:
    '''Queries DB for specified Goal and returns full details as JSON data.'''

    try:
        goal = validate_and_get_by_id(Goal, goal_id)
    except (IDTypeError, DBLookupError) as err:
        abort(make_error_response(err, Goal, goal_id))
    
    return jsonify(TasksGoal(goal)), 200


##################
# Slackbot route #
##################

slackbot_bp = Blueprint('slackbot', __name__, url_prefix = '/slackbot')

@slackbot_bp.route('', methods = ['POST'])
def respond_to_bot() -> tuple[Response, Literal[200]]:
    '''Evaluates request JSON and returns DB query result for display in Slack.
    
    Expects a query for all tasks, all goals, or all tasks that are part of a
    specified goal.
    '''
    
    data = request.get_json()
    if 'event' not in data:
        # Slack API requires challenge response
        # Some verification should happen here for security, but ...
        return jsonify({'challenge':data['challenge']}), 200
    else:
        text = data['event']['text']

    if 'tasks' in text:
        resource, title = Task, None
    elif 'goals' in text:
        resource, title = Goal, None
    elif 'finish' in text:
        p = re.compile(r'.*finish\s')
        title = p.sub('',text)
        resource = Goal
    else:
        abort(make_error_response(ValueError, None, detail=(' Bot did not '
                                                    'recognize request.')))
    
    if title is None:
        return jsonify(make_slackbot_response(resource)), 200
    return jsonify(make_slackbot_response(resource, TasksGoal, title)), 200