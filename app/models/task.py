from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(280))
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
