from app import db
from app.models.task import Task 
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except: 
        abort(make_response({"message": f"task {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal: 
        abort(make_response({"message":f"task {goal_id} not found"}, 404))
    
    return goal 

def validate_task_ids(task_ids):
    try:
        task_ids = int(task_ids)
    except: 
        abort(make_response({"message": f"task {task_ids} invalid"}, 400))

    task_id = Task.query.get(task_ids)

    if not task_id: 
        abort(make_response({"message":f"task {task_ids} not found"}, 404))
    
    return task_id 

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return {
                "details": "Invalid data"
        }, 400
    else:
        new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    response = {
        "id": new_goal.goal_id,
        "title": new_goal.title
    }

    return make_response(jsonify({"goal": response}), 201)

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        goals_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title
            }
        )
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    goal = Goal.query.get(goal_id)

    response = {
            "id": goal.goal_id, 
            "title": goal.title,
    }

    return make_response(jsonify({"goal": response}))

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    response = {
            "id": goal.goal_id, 
            "title": goal.title,
    }

    return make_response(jsonify({"goal": response}))

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')

    return make_response(jsonify({"details": response})) 

@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    for task in request_body["task_ids"]:
        task = validate_task_ids(task)
        goal.tasks.append(task)
    
    # db.session.add(new_task)
    db.session.commit()

    response = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

    return make_response(jsonify(response), 200)

@goals_bp.route("<goal_id/tasks", methods=["GET"])
def 



