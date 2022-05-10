from flask import abort, make_response
from .task import Task
import os, requests
from dotenv import load_dotenv


def validate_task(id):
	try:
		id = int(id)
	except:
		return abort(make_response({"message": f"task {id} is invalid"}, 400))

	task = Task.query.get(id)

	if not task:
		abort(make_response({"message": f"task {id} not found"}, 404))

	return task

def post_slack_message(message):
	url = "https://slack.com/api/chat.postMessage"

	params = {"channel": "C03ERAGUTR8",
    "text": message}

	headers = {"Authorization":
    f"Bearer {os.environ.get('API_KEY')}"}

	requests.post(url, params=params, headers=headers)
