import json
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")