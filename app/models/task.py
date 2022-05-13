from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)

    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"))

    def to_dict(self):
        if self.goal_id: 
            return {"task": {
            "id": self.id, 
            "title": self.title, 
            "description": self.description, 
            "is_complete": self.is_complete, 
            "goal_id": self.goal_id}
            }
        return {"task": {
            "id": self.id, 
            "title": self.title, 
            "description": self.description, 
            "is_complete": self.is_complete}
        }

    def to_dict_basic(self):
        if self.goal_id: 
            return {
            "id": self.id, 
            "title": self.title, 
            "description": self.description, 
            "is_complete": self.is_complete, 
            "goal_id": self.goal_id
            }
        return {
            "id": self.id, 
            "title": self.title, 
            "description": self.description, 
            "is_complete": self.is_complete
        }
