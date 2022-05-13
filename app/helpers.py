from flask import make_response, abort
import requests
import os

def validate_record(record_id, cls ):
  try: 
    record_id = int(record_id)
  except:
    abort(make_response({"message": f'{cls.__name__} {record_id} invalid'}, 400))
  record = cls.query.get(record_id)
  
  if not record:
    abort(make_response({"message": f'{cls.__name__} {record_id} not found'}, 404))
  
  return record

def send_slack_message(slack_message):
  path = "https://slack.com/api/chat.postMessage"

  header = {"Authorization": os.environ.get("SLACK_AUTHENTICATION_TOKEN")}

  query_params = {
    "channel": "task-notifications",
    "text": slack_message
  }

  requests.post(path, headers=header, params=query_params)