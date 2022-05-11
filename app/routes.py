from flask import Blueprint, request, make_response, abort, jsonify
import requests
from sqlalchemy import asc
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import date
import os
import requests
import json

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# VALIDATE ID
def validate_id(id):
    if "/tasks" in request.path:
        try:
            task_id = int(id)
        except ValueError:
            abort(make_response(jsonify(f"Task {task_id} is invalid"), 400))
        task = Task.query.get(task_id)
        if not task:
            abort(make_response(jsonify(f"Task {task_id} not found"), 404))
        return task
    if "/goals" in request.path or "/goals/<goal_id>" in request.path:
        try:
            goal_id = int(id)
        except ValueError:
            abort(make_response(jsonify(f"Goal {goal_id} is invalid"), 400))
        goal = Goal.query.get(goal_id)
        if not goal:
            abort(make_response(jsonify(f"Goal {goal_id} not found"), 404))
        return goal

# VALIDATE REQUEST
def validate_request(request):
    request_body = request.get_json()
    if "/goals" in request.path:
        try:
            request_body["title"]
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400)) 
        return request_body
    # if request.path == "/goals":
    try:
        request_body["title"]
        request_body["description"]
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400)) 
    return request_body

# POST /tasks
@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = validate_request(request)
    try:
        completion_time = request_body["completed_at"]
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at = completion_time
        )
    except KeyError:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
        )
    db.session.add(new_task)
    db.session.commit()
    return make_response({"task": new_task.to_dict()}, 201)

# GET /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    # Pull query parameters from url
    title_param = request.args.get("title")
    description_param = request.args.get("description")
    is_complete_param = request.args.get("is_complete")
    sort_param = request.args.get("sort")
    # start the query
    tasks = Task.query
    # build up the search criteria based on params present
    if title_param:
        tasks = tasks.filter_by(title=title_param)
    if description_param:
        tasks = tasks.filter_by(description=description_param)
    if is_complete_param:
        tasks = tasks.filter_by(completed_at=is_complete_param)
    if sort_param == "asc":
        tasks = tasks.order_by(Task.title.asc())
    elif sort_param == "desc":
        tasks = tasks.order_by(Task.title.desc())
    # execute the search and return all records that meet the criteria built
    tasks = tasks.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

# GET /<task_id>
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_id(task_id)
    return {"task": task.to_dict()}

# PUT /<task_id>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(task_id)
    request_body = validate_request(request)
    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at = request_body["is_complete"]
    db.session.commit()
    return make_response(jsonify({"task": task.to_dict()}))

# DELETE /<task_id>
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})

# MARK COMPLETE
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_id(task_id)
    task.completed_at = date.today()
    db.session.commit()

    # Sends message to channel to congratulate on task completion
    channel_name = "task-notifications"
    headers = {"Authorization": os.environ.get("SLACK_AUTHORIZATION")}
    text = f"Someone just completed the task {task.title}"
    url = f"https://slack.com/api/chat.postMessage?channel={channel_name}&text={text}&pretty=1"
    response = requests.post(url, headers=headers)

    return make_response({"task": task.to_dict()})

# MARK INCOMPLETE
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_id(task_id)
    task.completed_at = None
    db.session.commit()
    return make_response({"task": task.to_dict()})

# ------- GOALS ROUTES -------

# POST /goals
@goals_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = validate_request(request)
    new_goal = Goal(
        title=request_body["title"]
    )
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal": new_goal.to_dict()}, 201)

# GET /goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    # Pull query parameters from url
    title_param = request.args.get("title")
    # start the query
    goals = Goal.query
    # build up the search criteria based on params present
    if title_param:
        goals = goals.filter_by(title=title_param)
    # execute the search and return all records that meet the criteria built
    goals = goals.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

# GET /<goal_id>
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_id(goal_id)
    return {"goal": goal.to_dict()}

# PUT /<goal_id>
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_id(goal_id)
    # goal = Goal.query.get(goal_id)
    request_body = validate_request(request)
    goal.title = request_body["title"]
    db.session.commit()
    return make_response(jsonify({"goal": goal.to_dict()}))

# DELETE /<task_id>
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'})