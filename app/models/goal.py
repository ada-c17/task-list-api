from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy = True)


    def to_dict(self):
        return dict(goal=({
            "id" : self.goal_id,
            "title": self.title
        }))


    def goal_and_tasks_info(self):
        goal_info = self.to_dict()["goal"]
        tasks_info = [task.dict_rel()["task"] for task in self.tasks]
        goal_info["tasks"] = tasks_info
        return goal_info


    def task_ids(self):
        task_ids = []
        for task in self.tasks:
            task_ids.append(task.task_id)
        return task_ids

    