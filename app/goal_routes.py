from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from .routes_helper import validate_goal_id, create_message
from app import db


bp = Blueprint("goals", __name__, url_prefix="/goals")


@bp.route("", methods=("POST",))
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        create_message("Invalid data", 400)

    goal = Goal.from_dict(request_body)
    db.session.add(goal)
    db.session.commit()

    return make_response(jsonify(), 201)