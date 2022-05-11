from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    # def to_dict(self):
    #     tasks_list = []
    #     for task in self.tasks:
    #         tasks_list.append(task.to_dict_basic())
    
    #     return {
    #         "tasks": {
    #         "id": self.task.task_id,
    #         "goal_id": self.task.goal_id,
    #         "title": self.task.title,
    #         "description": self.task.description,
    #         "is_complete": bool(self.task.completed_at)
    #         }
    #     }
        