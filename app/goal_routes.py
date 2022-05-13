from flask import Blueprint, jsonify, request 
from app import db
from app.models.goal import Goal
from sqlalchemy import asc
from app.task_routes import validate_task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return jsonify({"msg" : f"'{goal_id}' is invalid"}), 400

    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify({"message" : f"Could not find '{goal_id}'"}), 404
    return goal

def format_goal(goal):
    return {
        "goal": {
            "id" : goal.goal_id,
            "title" : goal.title
                }
        }

@goals_bp.route('', methods=['POST'])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {
            "details" : "Invalid data"
        }, 400

    new_goal = Goal(
        title = request_body['title']
    )

    db.session.add(new_goal)
    db.session.commit()

    return format_goal(new_goal), 201

@goals_bp.route('', methods=['GET'])
def get_goals():
    goals = Goal.query.order_by(asc(Goal.title)).all()
    goals_response = []

    for goal in goals:
        goals_response.append(
            {
            "id" : goal.goal_id,
            "title" : goal.title
            }
        )
    return jsonify(goals_response), 200

@goals_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    if isinstance(goal, Goal):
        return format_goal(goal), 200
    return goal

@goals_bp.route('/<goal_id>', methods=['PUT'])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    if isinstance(goal, Goal):
        goal.title = request_body["title"]
        db.session.commit()
        
        return format_goal(goal), 200
    return goal

@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    if isinstance(goal, Goal):
        db.session.delete(goal)
        db.session.commit()
        return {
            "details" : f'Goal {goal_id} "{goal.title}" successfully deleted'
        }
    return goal

@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def assign_task_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    
    if isinstance(goal, Goal):
        tasks = []
        for task_id in request_body['task_ids']:
            task = validate_task(task_id)
            task.goal_id = goal_id
            tasks.append(task.task_id)
        db.session.commit()

        return {
            "id" : goal.goal_id,
            "task_ids" : tasks
        }
    return goal

@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_tasks_of_goal(goal_id):
    goal = validate_goal(goal_id)

    if isinstance(goal, Goal):
        tasks = []
        for task in goal.tasks:
            tasks.append({
                "id" : task.task_id,
                "goal_id" : task.goal_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : bool(task.completed_at)
            })

        return {
            "id" : goal.goal_id,
            "title" : goal.title,
            "tasks" : tasks
        }
    return goal