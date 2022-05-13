
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from .helper import validate_task, validate_goal, call_slack
from datetime import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


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
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)
    if task.completed_at:
        task.completed_at = None
        db.session.commit()

    return read_one_task(task_id)

# Update: Mark Complete on an Incompleted Task
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)
    if not task.completed_at:
        
        call_slack(task.title)
        task.completed_at = datetime.utcnow()
        db.session.commit()
    return read_one_task(task_id)


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

#%%%%%%%%%%%%%%%%%%%%%%%%%wave 6 starts here
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal_id = int(goal_id)
    goal=validate_goal(goal_id)
    request_body=request.get_json()
    
    for task_id in request_body["task_ids"]:
        new_task=validate_task(task_id)
        new_task.goal=goal   # this is very easy to miss out!!!
    db.session.commit()
    tasks = goal.tasks
    my_task_list=[task.task_id for task in tasks]
    
    return {"id":goal_id, 
            "task_ids": my_task_list}, 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal(goal_id):
    goal_id = int(goal_id)
    goal=validate_goal(goal_id)
    task_list=[]
    tasks = Task.query.filter_by(goal_id=goal_id)
    for task in tasks:
        task_list.append(task.to_json())
        
    return {"id": goal_id,
            "title": goal.title,
            "tasks": task_list}, 200
    

@goal_bp.route("/tasks/<goal_id>", methods=["GET"])
def get_tasks_includes_goal_ID(goal_idd):
    goal = validate_goal(goal_idd)
    # goalID_query = request.args.get("goal_id")
    tasks = Task.query.filter_by(goal_id=goal_idd)
    

    return {"task": tasks.to_json()}, 200
