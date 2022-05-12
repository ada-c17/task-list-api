from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates= "goal", lazy=True)


def to_dict(self):
    return {
        "goal":{
        "id":self.goal_id,
        "title":self.title }
    }