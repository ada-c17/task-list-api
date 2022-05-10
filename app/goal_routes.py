from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# Create a goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({
            "details": "Invalid data"
            }, 400)

    new_goal = Goal(title=request_body["title"])
                    
    db.session.add(new_goal)
    db.session.commit()

    return make_response(
        jsonify({
            "goal": {
                "id": new_goal.goal_id,
                "title": new_goal.title,
            }
        }), 
        201)

# Send list of task IDs to a goal
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_task_ids(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        goal.tasks.append(Task.query.get(task_id))

    db.session.commit()
    
    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }



# Getting saved goals/ no saved goals
@goals_bp.route("", methods=["GET"])
def getting_goals():
    sort = request.args.get("sort")
    if sort == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif sort == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
        })

    return jsonify(goals_response)


# Get one goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({}, 404)

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }
    }


# Update goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    request_body = request.get_json()
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({}, 404)

    goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
        }
    }


# Delete goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({}, 404)
    db.session.delete(goal)
    db.session.commit()

    return make_response({
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
        })

# Getting tasks for goal
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def getting_tasks_for_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({}, 404)
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "goal_id": task.goal_id,
            "is_complete": task.completed_at is not None
        })

    return {
        "id": goal.goal_id,
        "tasks": tasks_response,
        "title": goal.title
    }