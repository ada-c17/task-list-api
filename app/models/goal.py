from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return {
                "id": self.goal_id,
                "title": self.title,
                }

    def get_task_ids(self):
        tasks_id_list = []
        for task in self.tasks:
            tasks_id_list.append(task.task_id)
        return tasks_id_list

    def get_tasks(self):
        tasks_list = []
        for task in self.tasks:
            tasks_list.append(task.to_dict_with_goal_id())
        return tasks_list
        
    @classmethod
    def create(cls, request_body):
        return cls(
        title=request_body["title"]
    )