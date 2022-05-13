from app import db
from .task import Task
from sqlalchemy.orm import relationship

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy = True)

    def to_json(self):
        return dict(
            id=self.goal_id,
            title=self.title,
        )

