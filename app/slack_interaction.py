from __future__ import annotations
from typing import Any, Optional

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
