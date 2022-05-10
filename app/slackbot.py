import os
import requests
from dotenv import load_dotenv

load_dotenv()


def post_to_slack(task):
    url = "https://slack.com/api/chat.postMessage"

    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    post_headers = {
        "Authorization": os.environ.get("SLACK_API_KEY")
    }

    response = requests.post(url, params=query_params, headers=post_headers)

    return response