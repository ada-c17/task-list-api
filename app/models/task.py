from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = False
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_json(self):
        task_dict = { 
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete" : self.is_complete
                }
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    def written_out(cls):
        return "task"

    def update(self,req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]

        if req_body.get("completed_at"):
            self.is_complete = True
            self.completed_at = datetime.now()


    @classmethod
    def create(cls,req_body):
        new_task = cls(
            title=req_body['title'],
            description=req_body['description'],
        )
        return new_task