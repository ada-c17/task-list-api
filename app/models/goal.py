from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goals", lazy = True)

    def to_dictionary(self):
        goal_dict = {
            "id": self.goal_id,
            "title": self.title
        }

        if self.tasks:
            goal_dict["tasks"] = [task.task_id for task in self.tasks]

        return goal_dict