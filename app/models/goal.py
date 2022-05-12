from app import db
from sqlalchemy.orm import relationship


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title
        }
