from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def create_goal_dict(self):
        goal_dict = {
                    "id": self.goal_id,
                    "title": self.title,
                }
        return goal_dict