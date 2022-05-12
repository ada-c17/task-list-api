from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_json(self):
        return {"id": self.goal_id,
                "title": self.title
                }

    def update(self, req_body):
        self.title = req_body["title"]

    @classmethod
    def create(cls, req_body):

        new_goal = cls(
            title = req_body['title']
        )

        return new_goal
