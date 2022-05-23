from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task',backref="goal",lazy=True)

    def __repr__(self) -> str:
        return str(self)
        
    def __str__(self) -> str:
        return f'Goal ID {self.goal_id}, Title {self.title}, Tasks{self.tasks}'

    def to_dict(self):
        tasks_info = [task.to_dict() for task in self.tasks]
        return dict(
            id=self.goal_id,
            title=self.title,
    )

    @classmethod
    def from_dict(cls, data_dict):
        return Goal(title=data_dict["title"]) 

    def replace_details(self, data_dict):
        self.title=data_dict['title']