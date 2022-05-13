from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dictionary(self):
        # if self.completed_at:
        #     completed = True
        # else:
        #     completed = False
        response = {
            "id" : self.id,
            "title" : self.title
        #     "tasks" : self.tasks if self.tasks else None
        }
        if self.tasks:
            response["tasks"] = self.tasks

        return response

    @classmethod
    def from_dict(cls, data_dict):
        return Goal(title=data_dict["title"])