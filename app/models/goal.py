from app import db



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", lazy = True, backref="goal")


    def to_dict(self):
        return dict(goal=({
            "id" : self.goal_id,
            "title": self.title
        }))

    def task_ids(self):
        task_ids = []
        for task in self.tasks:
            task_ids.append(task.task_id)
        return task_ids

    def goal_to_task(self):
        goal_description = self.to_dict()["goal"]
        task_description = [task.dict()["task"] for task in self.tasks]
        goal_description["tasks"] = task_description
        return goal_description
