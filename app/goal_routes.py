from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.goal import Goal
from app.task_routes import validate_task_id

def validate_goal_id(goal_id):
    try: 
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"msg":f"The goal with id {goal_id} is not found"}, 400))
    goal = Goal.query.get(goal_id)
    if goal: 
        return goal

    abort(make_response({"msg":f"The goal with id {goal_id} is not found"}, 404))

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}), 400
    
    new_goal = Goal(
        title=request_body["title"]
        )
    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.to_dict()), 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals_response = []
    goals = Goal.query.all()
    for goal in goals:
        goals_response.append(goal.to_dict_basic())

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal_id(goal_id)

    return jsonify(goal.to_dict())

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_task(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit() 

    return jsonify(goal.to_dict())

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} \"{goal.title}\" successfully deleted'})

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    try:
        task_ids = request_body["task_ids"]
    except KeyError:
        return jsonify({"msg": "Missing task ids in request body"}), 400

    if not isinstance(task_ids, list): 
        return jsonify({"msg": "Expected list of task ids"}), 400

    tasks = []
    for id in task_ids:
        tasks.append(validate_task_id(id))

    response_task_ids = []
    for task in tasks:
        task.goal = goal
        response_task_ids.append(task.id)
    db.session.commit()

    response = {
        "id":goal.id, 
        "task_ids":response_task_ids
    }

    return jsonify(response)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_of_a_goal(goal_id):
    goal = validate_goal_id(goal_id)

    tasks_list = []
    for task in goal.tasks:
        task_dict = task.to_dict_basic()
        tasks_list.append(task_dict)

    return jsonify({
        "id":goal.id, 
        "title":goal.title, 
        "tasks":tasks_list
    })