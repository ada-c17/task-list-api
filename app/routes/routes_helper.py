from flask import jsonify, abort, make_response
from app.models.task import Task 
from app.models.goal import Goal

# Helper Functions
def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def get_record_by_id(cls,id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)
    
    model = cls.query.get(id)
    if model:
        return model

    error_message(f"No model of type {cls} with id {id} found", 404)

def get_task_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)
    
    task = Task.query.get(id)
    if task:
        return task

    error_message(f"Task with id {id} not found", 404)

def make_task_safely(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError as err:
        # error_message(f"Missing key: {err}", 400)
        error_message(f'Invalid data',400)
        
def replace_task_safely(task, data_dict):
    try:
        task.replace_details(data_dict)
    except KeyError as err:
        error_message(f"Invalid data",400)
    
def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)),status_code))

def make_goal_safely(data_dict):
    try:
        return Goal.from_dict(data_dict)
    except KeyError as err:
        # error_message(f"Missing key: {err}", 400)
        error_message(f'Invalid data',400)

def get_goal_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)
    
    goal = Goal.query.get(id)
    if goal:
        return goal

    error_message(f"Goal with id {id} not found", 404)

def make_goal_safely(data_dict):
    try:
        return Goal.from_dict(data_dict)
    except KeyError as err:
        # error_message(f"Missing key: {err}", 400)
        error_message(f'Invalid data',400)
        
def replace_goal_safely(goal, data_dict):
    try:
        goal.replace_details(data_dict)
    except KeyError as err:
        error_message(f"Invalid data",400)

# Input: {'task_ids': [1, 2, 3]}
# Output: List of tasks
def get_task_from_dict(request_body):
    list_of_tasks = []
    task_ids = request_body['task_ids']
    for task_id in task_ids:
        task=get_task_record_by_id(task_id)
        list_of_tasks.append(task)
    return list_of_tasks