
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from .routes_helper import error_message, get_record_by_id, make_goal_safely, replace_goal_safely

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# POST /goals
@goals_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = make_goal_safely(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

# GET /goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    sort_param = request.args.get("sort")

    if sort_param == 'asc':
        goals = Goal.query.order_by(Goal.title.asc())
    elif sort_param == 'desc':
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    
    result_list = [goal.to_dict() for goal in goals]

    return jsonify(result_list)

# GET /goals/<id>
@goals_bp.route("/<id>", methods=["Get"])
def read_goal_by_id(id):
    goal = get_record_by_id(Goal, id)
    return jsonify({"goal":goal.to_dict()})

# PUT /goals/<id>
@goals_bp.route("/<id>", methods=["PUT"])
def replace_goal_by_id(id):
    request_body = request.get_json()
    goal = get_record_by_id(Goal, id)

    replace_goal_safely(goal, request_body)

    db.session.add(goal)
    db.session.commit()

    return jsonify({"goal":goal.to_dict()})

# DELETE /goals/<id>
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal_by_id(id):
    goal = get_record_by_id(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal.id} "{goal.title}" successfully deleted'})

# POST /goals/<id>/tasks
@goals_bp.route("/<id>/tasks", methods=["POST"])
def post_task_ids_to_goal(id):

    goal = get_record_by_id(Goal, id)
    request_body = request.get_json()

    task_ids = request_body["task_ids"]

    for id in task_ids:
        task = get_record_by_id(Task, id)
        task.goal = goal
    
    db.session.commit()

    task_list = [task.id for task in goal.tasks ]

    return(jsonify({"id":goal.id, "task_ids": task_list}))

# GET /goals/<id>/tasks
@goals_bp.route("/<id>/tasks", methods=["GET"])
def read_tasks_from_goal(id):
    goal = get_record_by_id(Goal, id)

    return jsonify(goal.to_dict_with_tasks())


