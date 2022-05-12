from flask import Blueprint, jsonify, request, make_response, abort
from app.models.goal import Goal
from app import db
from app.helper import validate
import datetime
import os
import requests

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", strict_slashes=False, methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    response = [goal.todict() for goal in goals]
    return jsonify(response), 200