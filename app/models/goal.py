from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy = True)

    def to_json(self):
        goal_dict = {
            "id":self.id,
            "title":self.title
            }
        return goal_dict