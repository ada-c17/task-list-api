from flask import abort, make_response
import os, requests

def validate_object(cls, id):
    try:
        id = int(id)
    except:
        return abort(make_response({"message": f"{cls.__name__.lower()} {id} is invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        abort(make_response({"message": f"{cls.__name__.lower()} {id} not found"}, 404))

    return obj

def post_slack_message(message):
	url = "https://slack.com/api/chat.postMessage"

	params = {"channel": "C03ERAGUTR8",
    "text": message}

	headers = {"Authorization":
    f"Bearer {os.environ.get('API_KEY')}"}

	requests.post(url, params=params, headers=headers)
