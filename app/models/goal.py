from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True) # create task id

    def g_json(self):
        return {
                "id": self.id,
                "title": self.title
                }

    @classmethod
    def create(cls, req_body):
        new_goal = cls(
            title = req_body["title"]
        )

        return new_goal

    def update(self,req_body):
        self.title = req_body["title"]
        