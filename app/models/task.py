from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey(
        'goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]

        if "goal_id" in request_body:
            self.goal_id = request_body["goal_id"]

    @classmethod
    def create(cls, request_body):
        if "completed_at" not in request_body:
            request_body["completed_at"] = None
        new_task = cls(title=request_body["title"],
                       description=request_body["description"],
                       completed_at=request_body["completed_at"])

        return new_task
