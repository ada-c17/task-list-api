from flask import Blueprint, jsonify, abort, make_response, request
from requests import session
from app.helpers import validate_task
from app.models.goal import Goal
from app import db
from .helpers import validate_task
from datetime import datetime
import requests, os

goal_bp = Blueprint("goal", __name__, url_prefix = "/goals")

# Create goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    
    new_goal = Goal.create(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_json()}),201)

