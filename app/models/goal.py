from app import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", lazy=True, back_populates="goal")

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title
        }
