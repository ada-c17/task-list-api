from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def return_goal_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }