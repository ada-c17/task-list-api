from sqlalchemy import true
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime
from tests.test_wave_01 import test_create_task_must_contain_description

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals",__name__, url_prefix="/goals")

#POST /tasks
@tasks_bp.route("", methods=("POST",))
def create_task():
    request_body = request.get_json()
    
    task=make_task_safely(request_body)

    db.session.add(task)
    db.session.commit()
    result={"task":(task.to_dict())}
    return jsonify(result), 201

#GET /tasks
@tasks_bp.route("",methods=["GET"])
def get_tasks():
    title_param = request.args.get("sort")

    if title_param == 'asc':
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif title_param == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
        
    result_list = [task.to_dict() for task in tasks]

    return (jsonify(result_list))

# GET /tasks/<task_id>
@tasks_bp.route("/<task_id>",methods=["GET"])
def get_task_by_id(task_id):
    task = get_task_record_by_id(task_id)
    result={"task":(task.to_dict())}
    return jsonify(result)

#PUT /tasks/<task_id>
@tasks_bp.route("/<task_id>",methods=["PUT"])
def replace_task_by_id(task_id):
    request_body = request.get_json()
    task = get_task_record_by_id(task_id)

    replace_task_safely(task, request_body)

    db.session.commit()
    result={"task":(task.to_dict())}
    return jsonify(result)

#DELETE /tasks/<task_id>
@tasks_bp.route("/<task_id>",methods=["DELETE"])
def delete_task_by_id(task_id):
    task = get_task_record_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    result={"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}
    return jsonify(result)
    # return make_response(f"Task with id {task_id} successfully deleted!")

#PATCH /tasks/<task_id>
@tasks_bp.route("/<task_id>",methods=["PATCH"])
def update_task_by_id(task_id):
    task = get_task_record_by_id(task_id)
    request_body = request.get_json()
    task_keys = request_body.keys()

    if "title" in task_keys:
        task.title = request_body["title"]
    if "description" in task_keys:
        task.description = request_body["description"]
    
    db.session.commit()
    return jsonify(task.to_dict)

#PATCH /tasks/<task_id>/mark_complete
@tasks_bp.route("/<task_id>/mark_complete",methods=["PATCH"])
def update_mark_as_complete_by_id(task_id):
    task = get_task_record_by_id(task_id)
    request_body = request.get_json()
    # task_keys = request_body.keys()

    if task.completed_at is not None:
        true = request_body[task]['is_complete'] 
        print(request_body[task]['is_complete'])
    db.session.commit()
    result={"task":(task.to_dict())}
    return jsonify(result)

# POST /goals
@goals_bp.route("", methods=("POST",))
def create_goal():
    request_body = request.get_json()
    
    goal=make_goal_safely(request_body)

    db.session.add(goal)
    db.session.commit()
    result={"goal":(goal.to_dict())}
    return jsonify(result), 201

#GET /goals
@goals_bp.route("",methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    
    result_list = [goal.to_dict() for goal in goals]

    return (jsonify(result_list))

# GET /goals/<goal_id>
@goals_bp.route("/<goal_id>",methods=["GET"])
def get_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)
    result={"goal":(goal.to_dict())}
    return jsonify(result)

#PUT /goals/<goal_id>
@goals_bp.route("/<goal_id>",methods=["PUT"])
def replace_goal_by_id(goal_id):
    request_body = request.get_json()
    goal = get_goal_record_by_id(goal_id)

    replace_goal_safely(goal, request_body)

    db.session.commit()
    result={"goal":(goal.to_dict())}
    return jsonify(result)

#DELETE /goals/<goal_id>
@goals_bp.route("/<goal_id>",methods=["DELETE"])
def delete_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    result={"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}
    return jsonify(result)
    # return make_response(f"Task with id {task_id} successfully deleted!")

#PATCH /goals/<goal_id>
@goals_bp.route("/<goal_id>",methods=["PATCH"])
def update_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)
    request_body = request.get_json()
    task_keys = request_body.keys()

    if "title" in task_keys:
        goal.title = request_body["title"]
    
    db.session.commit()
    return jsonify(goal.to_dict)
# POST /goals/<goal_id>/tasks
# @goals_bp.route("/<goal_id>/tasks", methods=("POST",))
# def create_goal():
#     request_body = request.get_json()
    
#     goal=make_goal_safely(request_body)

#     db.session.add(goal)
#     db.session.commit()
#     result={"goal":(goal.to_dict())}
#     return jsonify(result), 201

#GET /goals/<goal_id>/tasks
# @goals_bp.route("/<goal_id>tasks",methods=["GET"])
# def get_goals():
#     goals = Goal.query.all()
    
#     result_list = [goal.to_dict() for goal in goals]

#     return (jsonify(result_list))
# Helper Functions
def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

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