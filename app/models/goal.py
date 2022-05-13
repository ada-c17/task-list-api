from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='goal', lazy=True)


    def to_dict(self):
            return dict(
                id=self.id,
                title=self.title)
                



## ONE TO MANY RELATIONSHIP
# GOALS HAVE MANY TASKS
