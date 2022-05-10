from sqlalchemy import ForeignKey
from app import db
from flask import Blueprint, jsonify
import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    # Need to match the class name
    # goal = db.relationship("Goal", backref="tasks")


# https://stackoverflow.com/questions/60864838/flask-sqlalchemy-get-column-in-parent-table-as-child-model-attribute-by-one-to