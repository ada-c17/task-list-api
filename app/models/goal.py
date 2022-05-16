from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return {
                "id": self.goal_id,
                "title": self.title,
                }

    def get_task_ids(self):
        tasks_id_list = [task.task_id for task in self.tasks]
        return tasks_id_list

    def get_tasks(self):
        tasks_list = [task.to_dict() for task in self.tasks]
        return tasks_list
        
    @classmethod
    def create(cls, data_dict):
        return cls(
        title=data_dict["title"]
    )