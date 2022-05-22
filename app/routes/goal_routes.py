from asyncio import tasks
from sqlalchemy import true
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime
from tests.test_wave_01 import test_create_task_must_contain_description
from .routes_helper import ( 
    get_task_from_dict, 
    make_goal_safely, 
    get_goal_record_by_id, 
    make_task_safely,
    replace_goal_safely,
    get_task_record_by_id
)

bp = Blueprint("goals", __name__, url_prefix="/goals")

# POST /goals
@bp.route("", methods=("POST",))
def create_goal():
    request_body = request.get_json()
    
    goal=make_goal_safely(request_body)

    db.session.add(goal)
    db.session.commit()
    result={"goal":(goal.to_dict())}
    return jsonify(result), 201

#GET /goals
@bp.route("",methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    
    result_list = [goal.to_dict() for goal in goals]
    

    return (jsonify(result_list))

# GET /goals/<goal_id>
@bp.route("/<goal_id>",methods=["GET"])
def get_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)
    result={"goal":(goal.to_dict())}
    return jsonify(result)

#PUT /goals/<goal_id>
@bp.route("/<goal_id>",methods=["PUT"])
def replace_goal_by_id(goal_id):
    request_body = request.get_json()
    goal = get_goal_record_by_id(goal_id)

    replace_goal_safely(goal, request_body)

    db.session.commit()
    result={"goal":(goal.to_dict())}
    return jsonify(result)

#DELETE /goals/<goal_id>
@bp.route("/<goal_id>",methods=["DELETE"])
def delete_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    result={"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}
    return jsonify(result)
    # return make_response(f"Task with id {task_id} successfully deleted!")

#PATCH /goals/<goal_id>
@bp.route("/<goal_id>",methods=["PATCH"])
def update_goal_by_id(goal_id):
    goal = get_goal_record_by_id(goal_id)
    request_body = request.get_json()
    task_keys = request_body.keys()

    if "title" in task_keys:
        goal.title = request_body["title"]
    
    db.session.commit()
    return jsonify(goal.to_dict)

# POST /goals/<goal_id>/tasks
@bp.route("/<goal_id>/tasks", methods=("POST",))
def update_goal_with_tasks(goal_id):
    goal=get_goal_record_by_id(goal_id)
    
    request_body = request.get_json()

    new_task = get_task_from_dict(request_body)

    # task_ids = (request_body['task_ids'])
    for task_id in request_body['task_ids']:
        task = get_task_record_by_id(task_id)
        task.goal_id = goal.goal_id

    db.session.commit()
    
    result={'id':goal.goal_id,'task_ids':[task.task_id for task in goal.tasks]}
    print(result)
    return jsonify(result), 200

# GET /goals/<goal_id>/tasks
@bp.route("/<goal_id>/tasks",methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = get_goal_record_by_id(goal_id)
    request_body = request.get_json()
    tasks = []
    for task in goal.tasks:
        print(task.goal_id)
        tasks.append({
                "id": task.goal_id,
                "goal_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at is not None
            } )
    result={
            "id": goal.goal_id,
            "title": goal.title,
            "tasks":tasks}
            # "tasks":[
            # {
            #     "id": task.id,
            #     "goal_id": task.goal_id,
            #     "title": task.title,
            #     "description": task.description,
            #     "is_complete": task.is_complete
            # } for task in goal.tasks
            # ]}
    return (jsonify(result)), 200

