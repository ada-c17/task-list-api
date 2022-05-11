from datetime import datetime
from email import message
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from sqlalchemy import asc, desc
from app.models.goal import Goal
from app.models.task import Task

goal_bp = Blueprint('goals', __name__, url_prefix='/goals')

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response(jsonify({'details': 'Invalid data'}), 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        return abort(make_response(jsonify(f"Goal {goal_id} not found"), 404))
    
    return goal


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        new_goal = Goal(
            title = request_body["title"]
        )

        db.session.add(new_goal)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    sort_param = request.args.get("sort")

    goals = Goal.query

    if sort_param:
        if sort_param == 'asc':
            goals = Goal.query.order_by(asc(Goal.title))
        else:
            goals = Goal.query.order_by(desc(Goal.title))
    
    goals = goals.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    
    return {"goal": goal.to_dict()}

@goal_bp.route("/<goal_id>", methods=["PUT"])
def replace_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return {"goal": goal.to_dict()}

@goal_bp.route("/<goal_id>/mark_complete", methods=["PATCH"])
def complete_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    title = request_body.get("title")

    if title:
        goal.title = request_body["title"]

    db.session.commit()
    
    return {"goal": goal.to_dict()}

@goal_bp.route("/<goal_id>/mark_incomplete", methods=["PATCH"])
def incomplete_goal(goal_id):
    goal = validate_goal(goal_id)
    
    goal.completed_at = None

    db.session.commit()

    return {"goal": goal.to_dict()}

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({'details': f'Goal "{goal.title}" successfully deleted'})

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):

    goal = validate_goal(goal_id)

    tasks_response = []
    for task in goal.tasks:
        is_complete = bool(task.completed_at)
        tasks_response.append(
            {
            "id": task.task_id,
            "goal_id": goal.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete
            }
        )
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response})

# @goal_bp.route("/<goal_id>/tasks", methods=["POST"])
# def post_task_to_goal(goal_id):
#     request_body = request.get_json()
#     task_ids = request_body["task_ids"]
#     tasks_response = []

#     goal = validate_goal(goal_id)
    
#     for i in range(len(task_ids)):
#         next_task = task_ids[i]
#         goal.tasks = next_task

#         new_task = Task(
#             title = request_body["title"],
#             description = request_body["description"],
#             completed_at = request_body["completed_at"],
#             goal_id = goal.goal_id
#             )
#         print(f"{new_task=}")
#         db.session.add(new_task)
#         db.session.commit()

#         tasks_response.append(
#             goal.tasks
#         )

#     return make_response(jsonify({
#         "id": goal.goal_id,
#         "task_ids": tasks_response
#     }), 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_to_goal(goal_id):
    tasks_response = []
    request_body = request.get_json()

    goal = validate_goal(goal_id)
    task_ids = request_body["task_ids"]

    for i in range(len(task_ids)):
        task_id = task_ids[i]

        task = Task.query.get(int(task_id))
        
        goal.tasks.append(task)
        db.session.commit()

        tasks_response.append(
                task_id
            )

    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids": tasks_response
    }), 200)