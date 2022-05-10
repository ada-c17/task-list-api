import os
from slack import WebClient
from slack.errors import SlackApiError
from app.models.goal import Goal
from app.models.task import Task

def post_slack_msg(task):
    client = WebClient(token=os.environ.get("SLACK_OAUTH_TOKEN"))
    try:
        client.chat_postMessage(
            channel="#task",
            text=f"Someone just completed the task {task.title}")
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")