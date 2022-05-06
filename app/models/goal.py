from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_json(self):
        return {
            "goal_id": self.goal_id,
            "title": self.title
        }

    def update(self, request_body):
        self.title = request_body["title"]

    @classmethod
    def create(cls, request_body):
        new_goal = cls(title=request_body["title"])

        return new_goal
