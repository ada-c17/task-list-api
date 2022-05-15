from __future__ import annotations
from typing import Any, Type
Url = str

#############################
# Slack integration methods #
#############################

import os
import requests
import json
from app.models.task import Task
from app.models.goal import Goal, TasksGoal

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

def format_block(item: Task | Goal) -> dict:
    block = dict()
    block['type'] = 'section'
    block['text'] = dict()
    block['text']['type'] = 'mrkdwn'
    block['text']['text'] = f"*{item.title}* _ {item.description}_"
    return block

def make_slackbot_response(cls: Type[Task | Goal], goal_title: str, 
                            response_url: Url) -> bool:
    '''Posts a message to Slack in response to a specific query to the bot.
    
    (This doesn't work yet, but I don't think it's the code's fault ;) I think
    I just don't have app permissions set right in Slack. The route that calls
    this function works as expected when triggered from Postman.)
    '''
    
    if not goal_title:
        items = cls.query.all()
    else:
        items = cls.query.filter(cls.title.ilike(f"%{goal_title}%")).all()
    
    item_blocks = [format_block(item) for item in items]
    header_blocks = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":pencil:  Task List  :pencil:"
			}
		},
		{
			"type": "divider"
		}
    ]

    headers = {
        'Authorization': f'Bearer {os.environ.get("SLACKBOT_OAUTH_TOKEN")}'
    }
    message = {
        "text": "Here's your task list.", 
        "response_type": "ephemeral",
        "blocks": header_blocks.extend(item_blocks)
        }
    r = requests.post(
        response_url, 
        headers = headers,
        json = json.dumps(message)
    )
    return r.status_code == 200
