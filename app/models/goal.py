

from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_json(self):
        return {"id": self.goal_id,
                "title": self.title,
        }
    
    def to_json_tasks(self):
        return {"id": self.goal_id,
                "title": self.title,
                "tasks": [item.to_json() for item in self.tasks]
        }

    def update(self, req_body):
        self.title = req_body["title"]

    @classmethod
    def create(cls, req_body):
        new_goal = cls(
            title = req_body["title"]
        )

        return new_goal