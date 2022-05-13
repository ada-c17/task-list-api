from app import db
from datetime import datetime


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal") 


    def to_json(self, category=None):

        goal_dict = { 
                    "id": self.goal_id,
                    "title": self.title,
                    }

        if category == "tasks":
            goal_dict["tasks"] = [
                task.to_json() for task in self.tasks
            ]

        return goal_dict


    def update(self,req_body):
        self.title = req_body["title"]


    @classmethod
    def create(cls,req_body):
        new_goal = cls(
            title=req_body['title'],
        )
        return new_goal