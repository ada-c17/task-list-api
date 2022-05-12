from flask import jsonify, abort, make_response
from app.models.goal import Goal
from app.models.task import Task

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def get_record_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)

    model = cls.query.get(id)
    if model:
        return model

    error_message(f"No model of type {cls} with id {id} found", 404)

def make_task_safely(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)

def replace_task_safely(task, data_dict):
    try:
        task.replace_details(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)

def make_goal_safely(data_dict):
    try:
        return Goal.from_dict(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)

def replace_goal_safely(goal, data_dict):
    try:
        goal.replace_details(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)