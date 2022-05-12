from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self, is_complete):
        if self.goal_id:
            dict_vals = {
                "task": {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete
                }
                }
        else:
            dict_vals = {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete
            }
        
        return dict_vals