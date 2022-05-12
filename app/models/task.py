from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)

    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        return {"task": {
            "id": self.id, 
            "title": self.title, 
            "description": self.description, 
            "is_complete": self.is_complete}
        }

    def to_dict_basic(self):
        return {
            "id": self.id, 
            "title": self.title, 
            "description": self.description, 
            "is_complete": self.is_complete
        }
