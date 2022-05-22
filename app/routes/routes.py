from sqlalchemy import true
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime
from tests.test_wave_01 import test_create_task_must_contain_description
from .routes_helper import get_goal_record_by_id

# bp = Blueprint("goals",__name__, url_prefix="/goals")


# # POST /goals/<goal_id>/tasks
# @bp.route("/<goal_id>/tasks", methods=("POST",))
# def create_task_with_goal(goal_id):
#     goal=get_goal_record_by_id(goal_id)
    
#     request_body = request.get_json()

#     new_task = Task.from_dict(request_body)
#     new_task.goal = goal

#     db.session.add(new_task)
#     db.session.commit()
#     result={"id":goal_id,"task_ids":(new_task.to_dict())}
#     return jsonify(result), 201

# # GET /goals/<goal_id>/tasks
# @bp.route("/<goal_id>/tasks",methods=["GET"])
# def get_tasks_for_goal(goal_id):
#     # goals = Goal.query.all()
#     goal = get_goal_record_by_id(goal_id)
#     task_info = [task.to_dict() for task in goal.tasks]
#     result={"id":goal_id,"title":(goal_id.title),"tasks":[task_info]}
#     return (jsonify(result))
