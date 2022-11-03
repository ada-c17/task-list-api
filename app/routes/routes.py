from sqlalchemy import true
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime
from tests.test_wave_01 import test_create_task_must_contain_description
from .routes_helper import get_goal_record_by_id

# bp = Blueprint("goals",__name__, url_prefix="/goals")

# Recreated the Routes using Goal_Routes and Task_routes.py 

