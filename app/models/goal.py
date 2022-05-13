from app import db
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def goal_response_body_dict(self):
        response_goal = {
            "id": self.id,
            "title": self.title
        }
        return response_goal
