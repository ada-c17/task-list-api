from app import db
#from xmlrpc.client import Boolean


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    is_complete = db.Column(db.Boolean)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")
    

    # def to_dict(self):
    #     tasks_list = []
    #     for task in self.tasks:
    #         tasks_list.append(task.to_dict_basic())
    
    #     return {
    #         "tasks": {
    #         "id": self.task_id,
    #         "goal_id": self.goal_id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": bool(self.completed_at)
    #         }
    #     }
    # def to_dict(self):
    #     return {
    #         "task_id": self.task_id,
    #         "goal_title": self.goal.title,
    #         "goal_tasks": self.goal.tasks
    #     }

    # def to_dict_basic(self):
    #     return {
    #         "id": self.task_id,
    #         "title": self.title,
    #         "tasks": self.goal
    #     }