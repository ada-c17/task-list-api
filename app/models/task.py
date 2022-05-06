from pandas import describe_option
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=False)


    def to_dictionary(self):
        return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            completed_at = self.completed_at
        )
