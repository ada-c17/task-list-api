from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("/<goal_id>/tasks", methods=['POST'])
def assign_task(goal_id):
    pass