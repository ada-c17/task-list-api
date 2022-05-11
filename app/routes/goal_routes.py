from app.models.task import Task
from app import db
from app.models.goal import Goal
import os
import datetime

from ..helpers import validate_task
from flask import Blueprint, request, jsonify, make_response, abort

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goal_bp.route("", methods=["GET"])
def get_all_tasks():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        # complete = None
        # if goal.completed_at == None:
        #     complete = False
        # else:
        #     complete = True
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
        })

    return make_response(jsonify(goals_response), 200)


@goal_bp.route("/<goal_id>", methods=["GET"])
def handle_task(goal_id):
    goal = validate_task(goal_id)
    return make_response(jsonify(goal.to_json()), 200)
