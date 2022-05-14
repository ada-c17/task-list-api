from __future__ import annotations
from typing import Any, Mapping, Optional

########################################################
# extension of JSONEncoder class for Task List objects #
########################################################

from flask.json import JSONEncoder


class TaskListJSONEncoder(JSONEncoder):
    '''A JSONEncoder subclass for serializing Task and Goal objects.
    
    Extends the default encoder so that flask.jsonify can process objects of
    type Task and Goal. All other types are passed to the base JSONEncoder
    class.

    Also recognizes a TasksGoal type used for alternate representation of Goal 
    objects with their associated Task objects.
    '''

    def default(self, obj: Any) -> dict[str, Any] | str | Any:
        '''Specifies how Task and Goal types should be represented in JSON.'''
        
        if type(obj).__name__ == 'Task':
            details = {
                'id': obj.task_id,
                'title': obj.title,
                'description': obj.description,
                'is_complete': obj.completed_at != None
            }
            if obj.goal_id:
                details['goal_id'] = obj.goal_id
            return details
        elif type(obj).__name__ == 'Goal':
            return {
                'id': obj.goal_id,
                'title': obj.title
            }
        elif type(obj).__name__ == 'TasksGoal':
            return {
                'id': obj._.goal_id,
                'title': obj._.title,
                'tasks': obj._.tasks
            }
        return JSONEncoder.default(self, obj)


###########################################
# Shared validation and filtering methods #
###########################################

from app.error_responses import IDTypeError, DBLookupError
from app.models.goal import Goal
from app.models.task import Task

def validate_and_get_by_id(cls, target_id: str | int) -> Task | Goal:
    '''Validates search id and returns result of database query.'''

    try:
        target_id = int(target_id)
    except:
        raise IDTypeError
    target = cls.query.get(target_id)
    if not target:
        raise DBLookupError
    return target


def get_filtered_and_sorted(cls, request_args: Mapping) -> list[Task | Goal]:
    '''Builds SQL query from request params. Returns the result of DB query.'''

    params = dict(request_args)  # Conversion to make request.args mutable
    sort_style = params.pop('sort', None)
    if sort_style not in {None, 'asc', 'desc'}:
        sort_style = None
    if sort_style and len(params) == 0: # just sort
        return cls.query.order_by(getattr(cls.title,sort_style)()).all()
    
    # make query filters from these 3 params, ignoring any others
    filters = []
    if 'title' in params:
        filters.append(cls.title.ilike(f"%{params['title']}%"))
    if 'description' in params:
        filters.append(cls.description.ilike(f"%{params['description']}%"))
    if 'is_complete' in params:
        if params['is_complete'] == 'False':
            filters.append(cls.completed_at == None)
        else:
            filters.append(cls.completed_at != None)
    filters = tuple(filters)
    
    if not sort_style:
        return cls.query.filter(*filters).all() # just filter
    return (cls.query.filter(*filters)
                            .order_by(getattr(cls.title,sort_style)()).all())


#############################
# Slack integration methods #
#############################

import os
import requests
from flask import jsonify

def notify(title: str, event: str, text: str = None) -> bool:
    '''Posts a message to Slack when a task is marked complete or incomplete.'''

    if not text and event == 'mark_complete':
        text = f'Someone just completed the task {title}'
    elif not text and event == 'mark_incomplete':
        text = f'Someone just marked the task {title} incomplete!'
    elif not text:
        text = f'Something labeled "{event}" just happened.'

    headers = {
        'Authorization': f'Bearer {os.environ.get("SLACKBOT_OAUTH_TOKEN")}'
    }
    params = {
        'text': text,
        'channel': 'task-notifications'
    }
    r = requests.post(
        'https://slack.com/api/chat.postMessage', 
        params = params, 
        headers = headers
    )
    return r.status_code == 200

def make_slackbot_response(cls, goal_wrapper: Optional[Any] = None, goal_title: str = None) -> bool:
    '''Posts a message to Slack in response to a specific query to the bot.
    
    (This doesn't work yet, but I don't think it's the code's fault ;) I think
    I just don't have app permissions set right in Slack. The route that calls
    this function works as expected when triggered from Postman.)
    '''

    if not goal_title:
        items = cls.query.all()
    else:
        goals = cls.query.filter(cls.title.ilike(f"%{goal_title}%")).all()
        items = [goal_wrapper(goal) for goal in goals]
    
    # TODO: Just raw JSON currently, make pretty for Slack message
    text = str(jsonify(items).get_json())

    headers = {
        'Authorization': f'Bearer {os.environ.get("SLACKBOT_OAUTH_TOKEN")}'
    }
    params = {
        'text': text,
        'channel': 'task-notifications'
    }
    r = requests.post(
        'https://slack.com/api/chat.postMessage', 
        params = params, 
        headers = headers
    )
    return r.status_code == 200
