from flask import Blueprint, jsonify, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from ..models.helpers import post_slack_message, validate_task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
