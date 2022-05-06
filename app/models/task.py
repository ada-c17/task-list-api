from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String) #index=True, unique=True with or without don't work for unique value
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    