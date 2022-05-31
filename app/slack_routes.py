from typing import Literal
from flask import Blueprint, Response, jsonify, request, abort
from app import db
from datetime import datetime
from app.models.task import Task
from app.models.goal import Goal
from app.commons import validate_and_get_by_id, get_filtered_and_sorted
from app.slack_interaction import make_slackbot_response
from app.error_responses import make_error_response
import json

##################
# Slackbot route #
##################

slackbot_bp = Blueprint('slackbot', __name__, url_prefix = '/slackbot')

# TODO: Make this into 2 different routes -- pull out the button interaction
# and change POST url in slack app dashboard

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
            action = payload['actions'][0]['action_id'].split()
        except:
            abort(make_error_response(KeyError, None, detail=(f' payload = {payload}')))
        
        task = validate_and_get_by_id(Task, task_id)
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