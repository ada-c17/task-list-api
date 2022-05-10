from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)


    def to_dict(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=False if self.completed_at == None else self.completed_at
        )
        
    def override_task(self, data_dict):
        self.title = data_dict["title"]
        self.description = data_dict["description"]

    # @classmethod
    # def from_dict(cls, data_dict):
    #     return cls(
    #         dict(
    #             title=data_dict["title"],
    #             description=data_dict["description"],
    #             completed_at=data_dict["completed_at"])
    #     )