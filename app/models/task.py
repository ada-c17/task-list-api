from email.policy import default
from app import db

#  title, description, and completed_at.
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None) #time_date, need to have option for null or None
