from flask import Blueprint, make_response, request, jsonify, abort
from app.models.goal import Goal
from app import db
from flask import request
from datetime import datetime
from app.models.task import Task
# datetime.datetime.utcnow()

goal_bp = Blueprint("goal_bp", __name__, url_prefix = "/goals")


def validate_goal(id_):
    try:
        id_ = int(id_)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    

    goal = Goal.query.get(id_)
    # gets the whole row in db with that particular id

    if not goal:
        abort(make_response({"message": f"Goal {id_} not found"}, 404))
        
    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():

    request_body = request.get_json()

    try:
        new_goal = Goal.create(request_body)
   
    except KeyError:
        return abort(make_response({"details": "Invalid data"}, 400))

    
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify(new_goal.to_dict()), 201)



@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.id,
                "title": goal.title
            }
        )

    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_with_one_goal(goal_id):
    goal = validate_goal(goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(Task.to_json(task))
    # goal["tasks"] = tasks_response

    return jsonify({"id": goal.id, "title": goal.title, "tasks": tasks_response}), 200
    # return jsonify(goal), 200

@goal_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)

    return jsonify(goal.to_dict()), 200


@goal_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    
    request_body = request.get_json()

    goal.update(request_body)

    db.session.commit()

    return jsonify(goal.to_dict()), 200


@goal_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {id} \"{goal.title}\" successfully deleted"}), 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task_with_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    # new_task = Task.create(request_body)
    task_ids = request_body["task_ids"]
    
    for task_id in task_ids:
        task = Task.query.get(task_id)
        task.goal_id = goal_id
      
        db.session.commit()

    goal_response = {
                    "id": goal.id,
                    "task_ids": task_ids
                    }
   
    # return make_response(jsonify({"id": goal.id, "task_ids": task_ids}), 200)
    return make_response(jsonify(goal_response), 200)


