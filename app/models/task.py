from app import db

'''
Task is a todo list task
'''
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        d = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }

        if self.goal_id:
            d['goal_id'] = self.goal_id

        return d

    # def update(self, request_body):
    #     self.title = request_body["title"]
    #     self.description = request_body["description"]
    #     self.completed_at = request_body["completed_at"]

    # @classmethod
    # def create(cls, request_body):
    #     new_task = cls(
    #         title=request_body["title"],
    #         description=request_body["description"],
    #         completed_at = request_body["completed_at"]
    #     )
    #     return new_task