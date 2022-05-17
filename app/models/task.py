from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def is_complete(self):
        return self.completed_at != None

    def to_dict(self):
        dictionary = dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete(),
            goal_id=self.goal_id
        )

        if self.goal_id == None:
            del dictionary["goal_id"] 

        return dictionary

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            completed_at=data_dict["completed_at"] if "completed_at" in data_dict else None
        )