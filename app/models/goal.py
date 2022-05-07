from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def get_dict(self):
        return {
                    "id" : self.goal_id,
                    "title" : self.title
                }
        