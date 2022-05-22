from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    def __repr__(self) -> str:
        return str(self)
    def __str__(self) -> str:
        return f'Task ID {self.task_id}, Title {self.title}, Completed At{self.completed_at}'
    def to_dict(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at is not None
        
    )

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict['title'],
            description=data_dict['description'],
            completed_at=data_dict.get("completed_at", None)
        )
        

    def replace_details(self, data_dict):
        self.title=data_dict['title']
        self.description=data_dict['description']
        