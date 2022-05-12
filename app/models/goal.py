from app import db



class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")


    def to_dict(self):
        return {"goal": {
                        "id": self.id,
                        "title": self.title
                        }
                }


    def update(self, req_body):
        self.title = req_body["title"]


    @classmethod
    def create(cls, req_body):
        new_goal = cls(
            title=req_body["title"]
        )
        return new_goal