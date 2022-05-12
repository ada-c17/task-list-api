
from email.policy import default
from unittest.mock import DEFAULT
from app import db
from .goal import Goal
from sqlalchemy.orm import relationship

# DEFINING A MODEL
'''
Models in our Flask code will create a 
direct connection between the data modeled in our
database. We will create a class for each model. 
The class will define the state and behavior of our model.
'''
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goals = db.relationship("Goal", back_populates="task")

    def to_json(self):
            return  {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": False if not self.completed_at else True
            }
            

    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
        # self.completed_at = request_body["completed_at"]

    @classmethod
    def create(cls, request_body):
        new_task = cls(
        title = request_body['title'],
        description = request_body['description'],
        completed_at = request_body.get("completed_at", None)
        )

        return new_task

