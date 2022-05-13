from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),
    nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def create(cls, req_body):
        new_task = cls(
            title=req_body["title"],
            description=req_body["description"],
            completed_at = req_body.get("completed_at")
        )
        return new_task

    def to_json(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }

        if self.goal:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    def update(self, req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]
        self.completed_at = req_body.get("completed_at")