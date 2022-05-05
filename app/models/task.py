from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(280))
    completed_at = db.Column(db.DateTime, default = None)
