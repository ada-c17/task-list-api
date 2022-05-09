from flask import Blueprint
from requests import request
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
