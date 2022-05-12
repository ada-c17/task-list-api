
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from .helper import validate_task, validate_goal
from datetime import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
slack_bp = Blueprint("slacks", __name__,
                     url_prefix="/slack.com/api/chat.postMessage")

# Create a task
@task_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    if not request_body.get("title") or not request_body.get("description"):
        return {"details": "Invalid data"}, 400
    new_task = Task.create(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_json()}, 201

# Get all tasks, sort by task name
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sorting_query = request.args.get('sort')
    if sorting_query == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sorting_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks=Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200


# get_one_task
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return {"task": task.to_json()}, 200

# UPDATE task


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return {"task": task.to_json()}, 200

# Update: Mark Incomplete on a Completed Task


@task_bp.route("/<task_id>/mark_incomplete", methods=["PUT"])
def mark_incomplete(task_id):
    task = validate_task(task_id)
    if task.completed_at:
        task.completed_at = None
        db.session.commit()

    return read_one_task(task_id), 200

# Update: Mark Complete on an Incompleted Task


@task_bp.route("/<task_id>/mark_complete", methods=["PUT"])
def mark_complete(task_id):
    task = validate_task(task_id)
    if not task.completed_at:
        task.completed_at = datetime.utcnow()
        db.session.commit()
        # @slack_bp.route("/slack.com/api/chat.postMessage", methods=["POST"])
        # def send_slack(task_id):
        #     return {f"Someone just completed the task {task.title}"}
    return read_one_task(task_id), 200

# DELETE Task


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% goals start here
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# Create a goal
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if not request_body.get("title"):
        return {"details": "Invalid data"}, 400
    new_goal = Goal.create(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_json()}, 201

# Get all goals, or sort by goal name
@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals=Goal.query.all()
    goal_response = []
    for goal in goals:
        goal_response.append(goal.to_json())

    return jsonify(goal_response), 200


# get_one_goal
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return {"goal": goal.to_json()}, 200


# UPDATE goal
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.update(request_body)

    db.session.commit()

    return {"goal": goal.to_json()}, 200



# DELETE goal
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
