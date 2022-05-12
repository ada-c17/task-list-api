

from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, default=None)
    description = db.Column(db.String, default=None)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        if self.completed_at != None:
            return {"id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": True}
        elif self.goal_id != None:
            return {"id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False}
        else:
            return {"id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False}
    
    @classmethod
    def create(cls, req_body):
        if "completed_at" in req_body.keys():
            new_task = cls(title=req_body['title'],
                    description=req_body['description'],
                    completed_at=req_body["completed_at"])
        else:
            new_task = cls(title=req_body['title'],
                    description=req_body['description'])
        return new_task

    def update(self, req_body):
        if "completed_at" in req_body.keys():
            self.title = req_body["title"]
            self.description = req_body["description"]
            self.completed_at = req_body["completed_at"]
        else:
            self.title = req_body["title"]
            self.description = req_body["description"]
