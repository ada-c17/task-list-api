from app import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy = True)

    def to_json(self):
        goal_dict = {
            "id":self.id,
            "title":self.title
            }
        return goal_dict

    def update(self, request_body):
        self.title=request_body["title"]

    @classmethod
    def create(cls, request_body):
        new_goal = cls(
                title=request_body["title"])
        return new_goal