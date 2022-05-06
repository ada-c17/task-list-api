from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db
from datetime import datetime
import requests
import os

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')