import requests
import time
import json
import os

class SlackClient:

    def __init__(self):
        self.SLACK_API_KEY = os.environ.get("SLACK_API_KEY")
        self.headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.SLACK_API_KEY}"
            }

    def _send_notification(self, text):
        url = "https://slack.com/api/chat.postMessage"

        payload = {
            "channel": "task-notifications",
            "text": text}
        
        response = requests.post(
            url, data=json.dumps(payload), headers=self.headers)

        return response

    def send_notification(self, text):
        # to avoid API rate limit
        # these are the HTTP status codes that we are going to retry
        # 429 - too many requests
        # 502 - bad gateway
        # 503 - service unavailable
        RETRY_CODES = [429, 502, 503]
        retry_count = 0
        max_retries = 5
        wait_time = 2

        while retry_count <= max_retries:
            response = self._send_notification(text)
            if response.status_code == 200:
                print("Slackbot sucessfully sent a notifcation.")
                return True
            elif response.status_code in RETRY_CODES:
                time.sleep(wait_time)
                retry_count += 1
                wait_time *= 2
            else:
                print("Slackbot failed to send a notifcation.")
                return False

        print("Slackbot failed to send a notifcation.")
        return False
