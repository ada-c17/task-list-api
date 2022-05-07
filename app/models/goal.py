from app import db


class Goal(db.Model):
    expected_elements = {"title":str}

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    def make_response_dict(self):
        goal_dict = {
            "id": self.goal_id,
            "title": self.title,
        }
        return goal_dict