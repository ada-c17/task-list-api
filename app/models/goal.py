from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        return dict(
            id=self.goal_id,
            title=self.title,
        )

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
        )

    def replace_details(self, data_dict):
        self.title = data_dict["title"]

    def list_tasks(self):
        return dict(
            id=self.goal_id,
            task_ids=[task.task_id for task in self.tasks]
        )
    
    def to_dict_with_tasks(self):
        return dict(
            id=self.goal_id,
            title=self.title,
            tasks=[task.to_dict() for task in self.tasks]
        )