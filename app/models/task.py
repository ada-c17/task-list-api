from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=None)
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks", lazy=True)

    def make_dict(self):
        data_dict=dict(
                id=self.task_id,
                goal_id=self.goal_id,
                title=self.title,
                description=self.description, 
                is_complete = self.is_complete
            )

        return data_dict
    
    def replace_all_details(self, data_dict):
        self.title = data_dict["title"]
        self.description = data_dict["description"]
        if "completed_at" in data_dict:
            self.completed_at = data_dict["completed_at"]
            self.is_complete = True

    def mark_complete(self):
        self.is_complete = True
        self.completed_at = datetime.utcnow()
    
    def mark_incomplete(self):
        self.is_complete = False
        self.completed_at = None

    @classmethod
    def from_dict(cls, data_dict):
        is_complete = "completed_at" in data_dict
        return cls(is_complete=is_complete,
                   title=data_dict["title"], 
                   description=data_dict["description"],
                   completed_at=data_dict.get("completed_at"))