from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task_dict = dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=True if self.completed_at else False
            # is_complete = bool(self.completed_at) - this is using bool on it
        )

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        
        return task_dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            completed_at=data_dict["completed_at"] if "completed_at" in data_dict else None
        )

    def replace_details(self, data_dict):
        self.title=data_dict["title"]
        self.description=data_dict["description"]
        self.completed_at=data_dict["completed_at"] if "completed_at" in data_dict else None

    def mark_completed(self):
        # self.completed_at = func.now()
        self.completed_at = datetime.utcnow()

    def mark_incompleted(self):
        self.completed_at = None
