from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime) 
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

    def to_dict(self):
        status = True if self.completed_at is not None else False
        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": status
                }

    def to_dict_with_goal_id(self):
        status = True if self.completed_at is not None else False
        if self.goal_id == None:
            result = {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": status
                }
        else:
            result = {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": status
                }
        return result
