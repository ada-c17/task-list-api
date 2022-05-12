from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    tasks = db.relationship("Task", backref="goal")

    def to_dict(self):
        tasks_list = []
        for task in self.tasks:
            tasks_list.append(task.to_dict_basic())

        return{
            "id": self.id, 
            "title": self.title, 
            "tasks": tasks_list
        }
