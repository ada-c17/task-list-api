
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, default=None)
    description = db.Column(db.String, default=None)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        return {"id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False
        }
    
    def to_json_goal(self):
        return {"id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False
        }

    # def update(self, req_body):
    #     self.title = req_body["title"]
    #     self.description = req_body["description"]
