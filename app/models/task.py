from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        response_dict = dict(
                id=self.task_id,
                title=self.title,
                description=self.description,
                is_complete=self.completed_at is not None
            )

        if self.goal_id:
            response_dict["goal_id"] = self.goal_id

        return response_dict

    # create similar functions for task and goal, class for creation
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
                title=data_dict["title"],
                description=data_dict["description"],
                completed_at = data_dict.get("completed_at", None)
            )
        
    def override_task(self, data_dict):
        self.title = data_dict["title"]
        self.description = data_dict["description"]