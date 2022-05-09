from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal = db.relationship("Goal", back_populates = "tasks", lazy = True)
    
    def task_to_JSON(self):
        rsp = {"task":
            {"id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }}
        if self.goal_id:
            rsp["task"]["goal_id"] = self.goal_id
        
        return rsp