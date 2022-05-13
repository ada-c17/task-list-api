from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.goal import Goal

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal.to_dict()}

    return make_response(jsonify(response_body), 201)