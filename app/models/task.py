
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, default=None)
    description = db.Column(db.String, default=None)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
