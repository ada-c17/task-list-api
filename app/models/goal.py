from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    goal_title = db.Column(db.String)

    def to_dict(self, is_complete):
            return {
                "id": self.goal_id,
                "title": self.goal_title
            }