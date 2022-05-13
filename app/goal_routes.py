# import json
# import os
# import datetime
# from pandas import json_normalize
# import requests
# from urllib import response
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes import get_task, get_task_by_id, update_task_by_id
from .helper_routes import get_record_by_id


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

##CRUD
##CREATE : POST
@goals_bp.route("", methods=["POST"])
def manage_post_goals():
    request_body = request.get_json()
    title = request_body.get("title")

    if title is None:
        response_body = make_response(jsonify({"details": "Invalid data"}), 400)
        return response_body
    

    goals = Goal.from_dict(request_body)


    db.session.add(goals)
    db.session.commit()

    return jsonify({"goal":goals.to_dictionary()}), 201

#READ : GET
@goals_bp.route("", methods=["GET"])
def manage_get_goals():
    goals = Goal.query.all()
    goal_dictionary = [goal.to_dictionary() for goal in goals]

    return jsonify(goal_dictionary)



@goals_bp.route("/<id>", methods=["GET"])
def get_goal_by_id(id):
    goal = get_goal(id)
    # response_body = dict()
    # response_body = goal.to_dictionary()
    return jsonify({"goal":goal.to_dictionary()})


#UPDATE : PUT
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal_by_id(id):
    goal = get_goal(id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return get_goal_by_id(id)


#DELETE : DELETE
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal_by_id(id):
    goal = get_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}), 200)



#### FRIENDSHIP ROUTEs
@goals_bp.route("/<id>/tasks", methods=["POST"])
def post_tasks_for_goal(id):
    goal = get_goal(id)
    request_body = request.get_json()

    # print("~~~RQ_BOD", request_body)
    task_ids = request_body["task_ids"]
    # print(task_ids)
    # task_list = []

    for task_id in task_ids:
        task = get_task(task_id)
        # task_list.append(task.id)
        task.goal = goal
        # task.goal_id = goal.id
        update_task_by_id(task_id)
    
    # {goal.tasks.append(task) for task in task_list if task not in goal.task}
    # goal.tasks = request_body["tasks"]
    db.session.commit()
    
    return {"id": goal.id, "task_ids": task_ids}
    # return jsonify(dict("id: {goal.id}: task_ids: {task_ids}")),200


@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_tasks_for_goal(id):
    goal = get_record_by_id(Goal, id)
    tasks = Task.query.filter_by(id=goal.id)
    print("*******TASKS******",tasks)
    tasks_info = [task.to_dictionary_with_goal() for task in tasks]
    response_body = {
        "id" : goal.id,
        "title" : goal.title,
        "tasks" : tasks_info
    }

    # for task_id in goal.tasks:
    #     task = get_task(task_id)
    #     # task_list.append(task.id)
    #     task.goal = goal
    #     # task.goal_id = goal.id

    # response_body = dict()
    # response_body["tasks"] = goal.to_dictionary()
    # request_body = request.get_json()
    return jsonify(response_body)

## no request body ?
## response body returns {goal{tasks}}



## HELPER FUNCTIONS:
def get_goal(id):
    try:
        goal_id = int(id)
    except ValueError:
        abort(make_response(jsonify({"message": f"goal {id} invalid"}), 400))
    
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(jsonify({"message": f"goal {id} not found"}), 404))
    else: 
        return goal
