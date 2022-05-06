from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

bp = Blueprint("tasks", __name__, url_prefix="/tasks")