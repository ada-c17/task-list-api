from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        task = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }

        if self.goal_id:
            task["goal_id"] = self.goal_id

        return task

    # def update(self, request_body):
    #     self.title = request_body["title"]
    #     self.description = request_body["description"]
    #     # self.is_complete = request_body["completed_at"]
    #     self.completed_at = request_body["completed_at"]


    # @classmethod
    # def create(cls, request_body):
    #     new_task = cls(
    #         title=request_body["title"],
    #         description=request_body["description"],
    #         # is_complete = request_body["completed_at"]
    #         is_complete = request_body["is_complete"]
    #     )
    #     return new_task

