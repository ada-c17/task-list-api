from flask import Blueprint, abort, make_response,jsonify, request
import requests
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime  
import os
from dotenv import load_dotenv
load_dotenv()

SLACK_AUTH = os.environ.get("SLACK_AUTH")
SLACK_PATH = "https://slack.com/api/chat.postMessage"
# TASK ROUTES BEGIN ON LINE 42
tasks_bp = Blueprint("Tasks", __name__, url_prefix="/tasks")
# GOAL ROUTES BEGIN ON LINE 126
goals_bp = Blueprint("Goals", __name__, url_prefix="/goals")

#--------BEGIN HELPER FUNCTIONS----------
def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def update_task_safely(task, data_dict):
    try:
        task.update_self(data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}. Task not updated.", 400)
    except KeyError as err:
        error_message(f"Missing key(s): {err}. Task not updated.", 400)
        
def get_task_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response(jsonify(dict(details=f"Invalid id: {id}")),400))
    task = Task.query.get(id)
    if task:
        return task
    else:
        abort(make_response(jsonify(dict(details=f"Invalid id: {id}")),404))
#--------END HELPER FUNCTIONS----------


#--------BEGIN TASK ROUTES-------------
@tasks_bp.route("", methods=["GET",])
def get_tasks():
    sort_param = request.args.get("sort")
    if sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc()) 
    else:
        tasks = Task.query.all()
    response = [task.self_to_dict() for task in tasks]
    return make_response(jsonify(response))

@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = get_task_record_by_id(id)
    return jsonify(task=task.self_to_dict())

@tasks_bp.route("", methods=["POST",])
def add_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"]
                    )
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
    except KeyError:
        return make_response(jsonify(details="Invalid data"),400)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(task=new_task.self_to_dict()),201)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = get_task_record_by_id(id)

    request_body = request.get_json()

    update_task_safely(task, request_body)

    db.session.commit()

    return make_response(jsonify(task=task.self_to_dict()))

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def update_task_complete(id):
    task = get_task_record_by_id(id)
    task.completed_at = datetime.now()
    db.session.commit()

    header_params = {"Authorization": SLACK_AUTH}
    query_params = {
        "channel": "test-channel",
        "text": f"Task marked complete: {task.title}"}
    requests.post(SLACK_PATH, params=query_params, headers=header_params)

    return make_response(jsonify(task=task.self_to_dict()))

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def update_task_incomplete(id):
    task = get_task_record_by_id(id)
    task.completed_at = None
    db.session.commit()

    header_params = {"Authorization": SLACK_AUTH}
    query_params = {
        "channel": "test-channel",
        "text": f"Task marked incomplete: {task.title}"}
    requests.post(SLACK_PATH, params=query_params, headers=header_params)

    return make_response(jsonify(task=task.self_to_dict()))

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = get_task_record_by_id(id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify(details=f"Task {task.task_id} \"{task.title}\" successfully deleted"),200)

#--------END TASK ROUTES------------

#--------BEGIN GOAL ROUTES----------
def update_goal_safely(goal, data_dict):
    try:
        goal.update_self(data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}. Task not updated.", 400)
        
def get_goal_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response(jsonify(dict(details=f"Invalid id: {id}")),400))
    goal = Goal.query.get(id)
    if goal:
        return goal
    else:
        abort(make_response(jsonify(dict(details=f"Invalid id: {id}")),404))

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError as err:
        abort(make_response(jsonify(dict(details=f"Invalid data")),400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify(goal=new_goal.self_to_dict()),201)

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = get_goal_record_by_id(id)

    request_body = request.get_json()

    update_goal_safely(goal, request_body)

    db.session.commit()

    return make_response(jsonify(goal=goal.self_to_dict()),201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response = [goal.self_to_dict() for goal in goals]
    return jsonify(response)

@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = get_goal_record_by_id(id)
    return jsonify(goal=goal.self_to_dict())

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task_with_goal(goal_id):

    goal = get_goal_record_by_id(goal_id)
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"], goal=goal)
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
    except KeyError:
        return make_response(jsonify(details="Invalid data"),400)


    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify(f"Book {new_task.title} as part of the goal {new_task.goal.title} successfully created"), 201)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal(goal_id):

    goal = get_goal_record_by_id(goal_id)
    # sort_param = request.args.get("sort")
    # if sort_param == "desc":
    #     goals = Goal.query.order_by(Goal.title.desc())
    # elif sort_param == "asc":
    #     goals = Goal.query.order_by(Goal.title.asc()) 
    # else:
    #     response = [goal.self_to_dict() for goal in goals]
    # return make_response(jsonify(response))
    response = []
    for task in goal.tasks:
        response.append(
            {
            "id": task.id,
            "title": task.title,
            "description": task.description
            }
        )
    return jsonify(tasks=response)


@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = get_goal_record_by_id(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify(details=f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"),200)

