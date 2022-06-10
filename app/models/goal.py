from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def to_dictionary(self):
        return dict(
            id=self.goal_id,
            title=self.title
        )