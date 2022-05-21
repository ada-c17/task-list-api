from __future__ import annotations
from typing import Optional, Type
Url = str

#############################
# Slack integration methods #
#############################

import os
import requests
import json
from app.models.task import Task
from app.models.goal import Goal

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
    '''Formats details of input intp a markdown block for a Slack message.'''

    block = dict()
    block['type'] = 'section'
    block['text'] = dict()
    block['text']['type'] = 'mrkdwn'
    goal_title = ''
    if type(item) == Task:
        if item.completed_at != None:
            s, btn_text, btn_action = '~', 'Mark Incomplete', 'mark-incomplete'
        else:
            s, btn_text, btn_action = '', 'Mark Complete', 'mark-complete'
        if goal_title != '':
            command = '/finish'
        else:
            command = '/alltasks'

        block['text']['text'] = f"-   *{s}{item.title}{s}* _ {item.description}_"
        block['accessory'] = dict()
        block['accessory']['type'] = 'button'
        block['accessory']['text'] = dict()
        block['accessory']['text']['type'] = 'plain_text'
        block['accessory']['text']['text'] = btn_text
        block['accessory']['value'] = str(item.task_id)
        block['accessory']['action_id'] = f'{btn_action} {command} {goal_title}'
    else:
        block['text']['text'] = f"*{item.title}:* "
        goal_title = item.title

    return block

def make_slackbot_response(cls: Type[Task | Goal], goal_title: str, 
                            response_url: Url, include_complete: Optional[bool] = False) -> bool:
    '''Posts a message to Slack in response to a specific query to the bot.'''
    
    if not goal_title:
        items = cls.query.all()
    else:
        items = cls.query.filter(cls.title.ilike(f"%{goal_title}%")).all()
    
    blocks = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Task :relieved: :star: :ok: :star: :relieved: :star: :ok: :star: :relieved: List",
				"emoji": True
			}
		},
		{
			"type": "divider"
		}
    ]
    for item in items:
        if type(item) == Goal or item.completed_at == None or include_complete:
            blocks.append(format_block(item))
        if type(item) == Goal:
            try:
                for task in item.tasks:
                    if task.completed_at == None or include_complete:
                        blocks.append(format_block(task))
            except:
                blocks.append({"type":"divider"})
    
    headers = {
        'Authorization': f'Bearer {os.environ.get("SLACKBOT_OAUTH_TOKEN")}'
    }
    message = {
        "text": "Here's your task list.", 
        "response_type": "ephemeral",
        'channel': 'task-notifications',
        "blocks": json.dumps(blocks)
        }
    # print(json.dumps(blocks))
    r = requests.post(
        response_url, 
        headers = headers,
        json = message
    )
    return r