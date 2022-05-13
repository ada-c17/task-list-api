from app import db


class Goal(db.Model):
    __tablename__ = 'goals'
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goals")

    def to_dict(self):
        task_list = []
        for task in self.tasks:
            task_list.append(task.id)
        if task_list:
            return dict(
                id=self.goal_id,
                task_ids=task_list
            )
        return dict(
            id=self.goal_id,
            title=self.title)
    
    def get_tasks(self):
        from .task import Task
        task_list = []
        for task in self.tasks:
            readable_task = task.task_to_dict()
            task_list.append(readable_task)
        return dict(
            id=self.goal_id,
            title=self.title,
            tasks=task_list)
    
    @classmethod
    def from_dict(cls, data_dict):
            return cls(title=data_dict["title"])
    
    def replace_details(self, data_dict):
        if "task_ids" in data_dict:
            from .task import Task
            for id in data_dict["task_ids"]:
                task = Task.query.get(id)
                if task not in self.tasks:
                    self.tasks.append(task)
        else:
            self.title=data_dict["title"]
        return self.to_dict()
