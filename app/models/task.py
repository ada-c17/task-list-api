from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    is_complete = db.Column(db.Boolean, default = False)

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    
    """
    --unused
    """
    # @classmethod
    # def create_complete(cls, request_body):
    #     new_task = cls(
    #         title=request_body["title"],
    #         description=request_body["description"],
    #         completed_at=request_body["completed_at"]
    #     )

    #     return new_task
    
    @classmethod
    def create(cls, request_body):
        new_task = cls(
            title=request_body["title"],
            description=request_body["description"],
            is_complete=request_body["is_complete"]
        )

        return new_task
    
    def to_json(self):
        return {
            "task": 
            {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete
            }
        }
