from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # PARENT - ONE TO MANY
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    # TURN INTO JSON
    def g_json(self):
        return {
            "id": self.id,
            "title": self.title
        }

    # CREATE GOAL
    @classmethod
    def create(cls, request_body):
        new_goal = cls(
            title = request_body["title"],
        )
        return new_goal


    # UPDATE GOAL
    def update(self, request_body):
        self.title =  request_body["title"]
        




