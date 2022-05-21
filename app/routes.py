from typing import Literal
from flask import Blueprint, Response, jsonify, request, abort
from app import db
from datetime import datetime
from app.models.task import Task
from app.models.goal import Goal, TasksGoal
from app.commons import validate_and_get_by_id, get_filtered_and_sorted
from app.slack_interaction import notify, make_slackbot_response
from app.error_responses import (MissingValueError, FormatError, DBLookupError,
                                IDTypeError, make_error_response)
import json

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
    
    return jsonify({'id': int(goal_id), 'task_ids': [task.task_id for task in goal.tasks]}), 200

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
    '''Evaluates request body and returns DB query result for display in Slack.
    
    Expects a query for incomplete tasks, all tasks, all goals, all tasks that
    are part of a specified goal, task creation, and task assignment to goal.

    Also handles requests to update a task's completion status.
    '''
    
    if request.mimetype == 'application/json' and 'challenge' in request.json:
        # Slack API requires challenge response
        return jsonify({'challenge':request.json['challenge']}), 200
    else:
        data = request.form
    
    valid_commands = {'/tasks', '/goals', '/finish', 
                    '/addtask', '/alltasks', '/addtogoal'}
    if data.get('payload', None):
        payload = json.loads(data['payload'])
        try:
            task_id = payload['actions'][0]['value']
        except:
            abort(make_error_response(KeyError, None, detail=(f' payload = {payload}')))
        action = payload['action_id'].split()
        try:
            task = validate_and_get_by_id(Task, task_id)
        except (IDTypeError, DBLookupError) as err:
            abort(make_error_response(err, Task, task_id))
        
        task.completed_at = datetime.utcnow() if action[0] == 'mark-complete' else None
        db.session.commit()
        command = action[1]
        text = action[2] if command == '/finish' else ''
        url = payload['response_url']
    elif (not (command := data.get('command', None)) or 
            command not in valid_commands):
        abort(make_error_response(ValueError, None, detail=(f' Bot did not '
                                                f'recognize request: {command}'
                                                    f' provided as command.')))
    else:
        text = data['text'] if command in ('/finish', '/addtask', '/addtogoal') else ''
        url = data['response_url']
    resource = Goal if command in ('/goals', '/finish', '/addtogoal') else Task
    
    if command == '/addtask':
        details = text.split(',')
        details_dict = {
            "title": details[0],
            "description": details[1].strip() if len(details) > 1 else None
        }
        new_task = Task.create(details_dict)
        db.session.add(new_task)
        db.session.commit()
        text = ''
    if command == '/addtogoal':
        details = text.split(',')
        task = get_filtered_and_sorted(Task,{'title':details[0]})[0]
        goal = get_filtered_and_sorted(Goal, {'title': details[1].strip()})[0]
        goal.tasks.append(task)
        db.session.commit()
        text = details[1].strip()
    
    include_complete = command in ('/alltasks', '/finish') 
    r = make_slackbot_response(resource, text, url, include_complete)
    if r.status_code == 200:
        return jsonify({"response_type": "ephemeral", "text": "There you go", "slack_response": r.text}), 200
    else:
        return jsonify(r.text), 400