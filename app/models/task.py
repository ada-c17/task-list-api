from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks", lazy=True)

    def is_complete(self):
        return self.completed_at is not None

    def to_dict(self):
        
        if self.goal_id is None:
            return {"id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": self.is_complete()
            }
        else:
            return {"id": self.id,
                    "goal_id": self.goal_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": self.is_complete()
            }
            