
from flask import jsonify, abort, make_response
import os
import requests


def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def success_message_info_as_list(message, status_code=200):
    return make_response(jsonify(message), status_code)

# def return_database_info_list(return_value):
#     return make_response(jsonify(return_value))

def return_database_info_dict(category, return_value):
    return_dict = {}
    return_dict[category] = return_value
    return make_response(jsonify(return_dict))

def get_record_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id: {id}", 400)
    record = cls.query.get(id)
    if record:
        return record
    else:
        error_message(f"{cls.return_class_name()} id: {id} not found", 404)

def create_record_safely(cls, data_dict):
    try:
        return cls.create_from_dict(data_dict)
    except ValueError as err:
        error_message(f"Invalid data", 400)
    # I'm not sure the below error will ever actually come about with how my create_from_dict functions are structured.
    # However, I'm leaving it in as a reflection of how I would choose to structure error messages if left to my own devices
    except KeyError as err:
        error_message(f"Invalid key(s): {err}.  {cls.return_class_name()} not added to {cls.return_class_name()} List.", 400)

def update_record_safely(cls, record, data_dict):
    try:
        record.update_self(data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}. {cls.return_class_name()} not updated.", 400)
    except KeyError as err:
        error_message(f"Missing key(s): {err}. {cls.return_class_name()} not updated.", 400)

def send_slackbot_message(task_title):
    path = "https://slack.com/api/chat.postMessage"
    slackbot_key = os.environ.get("SLACK_OAUTH_TOKEN")
    headers = {'authorization': f'Bearer {slackbot_key}'}
    params = {
        'channel' : 'task-notifications',
        'text' : f'Someone just completed task {task_title}! :tada::tada::tada:',
    }
    requests.patch(path, headers=headers, params=params)



