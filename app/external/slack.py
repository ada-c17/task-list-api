import os
import requests

TOKEN = os.environ.get("SLACK_BOT_TOKEN")

def notify_completed(task_title):
    data = {
        "channel": "test-channel",
        "text": f"Someone just completed the task {task_title}"
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    requests.post('https://slack.com/api/chat.postMessage', data = data, headers = headers)
