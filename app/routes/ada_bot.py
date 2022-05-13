import os
import requests
import time

def send_msg_completed_task(task_title):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_BOT_TOKEN")


    params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task_title}"
    }
    headers = {
        # "Content-type": "application/json", does not work
        # "Authorization": "Bearer" + " " + SLACK_API_KEY
        "Authorization": f"Bearer {SLACK_API_KEY}"
    }

    requests.post(PATH, data=params, headers=headers)

    time.sleep(1) 