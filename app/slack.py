import os
from dotenv import load_dotenv
import requests

# load_dotenv()

SLACK_API_URL = "https://slack.com/api/chat.postMessage"


class SlackBot():
    def __init__(self):
        self.token = os.environ.get("SLACK_API_TOKEN")

    def send_notification(self, text):
        requests.post(SLACK_API_URL, headers={'Authorization': f"Bearer {self.token}"},
                      params={"channel": "task-notifications", "text": text})

