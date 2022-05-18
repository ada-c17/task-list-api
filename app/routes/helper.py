from flask import abort, make_response
from ..models.task import Task
from ..models.goal import Goal
import requests
import os


def validate_task(id):
	try:
		id = int(id)
	except:
		return abort(make_response({"message": f"task {id} is invalid"}, 400))

	task = Task.query.get(id)

	if not task:
		abort(make_response({"message": f"task {id} not found"}, 404))

	return task


def validate_goal(id):
	try:
		id = int(id)
	except:
		return abort(make_response({"message": f"goal {id} is invalid"}, 400))

	goal = Goal.query.get(id)

	if not goal:
		abort(make_response({"message": f"goal {id} not found"}, 404))

	return goal


def slack_bot(task):
	SLACK_BOT_POST_PATH = "https://slack.com/api/chat.postMessage"

	query_params = {
    "channel": "test-channel",
    "text": f"Someone just completed the task {task.title}"
	}
	headers = {"Authorization": os.environ.get("SLACK_BOT_KEY")}
    
	response_bot = requests.post(SLACK_BOT_POST_PATH, params=query_params, headers=headers)