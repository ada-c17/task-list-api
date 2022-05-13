from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task',backref="goal",lazy=True)

    def to_dict(self):
        return dict(
            id=self.goal_id,
            title=self.title,
    )

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict['title'],
        )

    def replace_details(self, data_dict):
        self.title=data_dict['title']