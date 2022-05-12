from app import db

'''
"goal" = {
    "id": 1,
    "title": "Read 40 books in 2022"
}
'''

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_json(self):
        return {
            "goal": {
                "id": self.goal_id,
                "title": self.title
             }
        }