from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)

    title = db.Column("title",db.String)

    description = db.Column("description", db.String)

    completed_at = db.Column("completed_at", db.DateTime, default = None)
