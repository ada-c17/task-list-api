from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy=True)


    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title
            )
            
    def to_dict_with_tasks(self):
        tasks_info = [task.to_dict() for task in self.tasks]
        return dict(
            id = self.id,
            title = self.title,
            tasks = tasks_info
        )

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
                title = data_dict["title"],
            )

    def replace_details(self, data_dict):
        self.title = data_dict["title"]

