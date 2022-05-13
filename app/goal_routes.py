from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from app.models.goal import Goal
from sqlalchemy import desc, asc, select


#Goals Blueprint

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

#helper functions
#validate goal id is int(id) or throw 400 for non int or 404 for int(id) not found
def validate_goal_id(goal_key):
    try:
        goal_key = int(goal_key)
    except:
        abort(make_response(dict(message=f"Goal {goal_key} is not an int."), 400))
    
    goal = Goal.query.get(goal_key)
    if not goal:
        return abort(make_response(dict(message=f"Goal {goal_key} is invalid."), 404))
    else:
        return goal


#CREATE/POST a Goal
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(
            title= request_body["title"]
        )

        db.session.add(new_goal)
        db.session.commit()
    except KeyError:
        return (dict(details=f"Invalid data"), 400)

    return jsonify(new_goal.to_dict()), 201

#GET/READ goals when there is at least one saved
@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals_response = []

    goal_query = request.args.get("title")
    goal_sort = request.args.get("sort")
        
    #filter by title key
    if goal_sort == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif goal_sort == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    elif goal_query:
        goals = Goal.query.filter_by(title=goal_query)
    else:
        goals = Goal.query.all()

    for goal in goals:
        goal_object = goal.to_dict()
        goals_response.append(goal_object["goal"])
    
    return jsonify(goals_response), 200

#GET/READ One goal
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal_by_id(goal_id):
    goal = validate_goal_id(goal_id)
    return jsonify(goal.to_dict()), 200

#UPDATE/PUT goal
@goal_bp.route("/<goal_key>", methods=["PUT"])
def replace_goal_by_id(goal_key):
    goal = validate_goal_id(goal_key)
    request_body = request.get_json()
    
    goal.title = request_body["title"]
    
    db.session.commit()

    return jsonify(goal.to_dict()), 200

#DELETE a goal by id
@goal_bp.route("/<goal_key>", methods=["DELETE"])
def delete_goal_by_id(goal_key):
    goal = validate_goal_id(goal_key)

    db.session.delete(goal)
    db.session.commit()

    return make_response(dict(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted'), 200)


#send a list of tasks to goal
#POST
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_list_for_goal(goal_id):
    from app.models.task import Task

    goal = validate_goal_id(goal_id)
    request_body = request.get_json()

    

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        goal.tasks.append(task)

    db.session.add(goal)
    db.session.commit()


    return jsonify({"id": goal.goal_id, "task_ids": goal.task_ids()}), 200
    

#GET/READ 
@goal_bp.route("/<goal_key>/tasks", methods=["GET"])
def get_goal_info(goal_key):
    goal = validate_goal_id(goal_key)

    return goal.goal_and_tasks_info(), 200










